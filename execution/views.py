# views.py that belongs to the execution app

import os
import csv
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from .models import PipelineRun


def run_detail(request, run_id):
    run = get_object_or_404(PipelineRun, id=run_id)

    output_files = []

    if run.status == "DONE" and run.work_dir and os.path.exists(run.work_dir):
        for root, dirs, files in os.walk(run.work_dir):
            dirs[:] = [d for d in dirs if d not in ["work", ".nextflow"]]
            for filename in files:
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, run.work_dir)
                output_files.append({
                    "name": relative_path,
                    "size_kb": round(os.path.getsize(filepath) / 1024, 2)
                })

    return render(request, "execution/run_detail.html", {
        "run": run,
        "output_files": output_files
    })


def download_file(request, run_id, filepath):
    run = get_object_or_404(PipelineRun, id=run_id)

    full_path = os.path.join(run.work_dir, filepath)
    full_path = os.path.abspath(full_path)

    if not full_path.startswith(os.path.abspath(run.work_dir)):
        raise Http404("File not found")

    if not os.path.exists(full_path):
        raise Http404("File not found")

    return FileResponse(open(full_path, "rb"), as_attachment=True, filename=os.path.basename(full_path))


# -------------------------------------------------------
# comparison views
# -------------------------------------------------------

def parse_quast_report(work_dir):
    """
    Reads QUAST/report/report.tsv and returns a dict like:
    { "Total length": "5200000", "N50": "450000", ... }
    Returns None if the file is not found.
    """
    quast_path = os.path.join(work_dir, "QUAST", "report", "report.tsv")

    if not os.path.exists(quast_path):
        return None

    stats = {}
    with open(quast_path, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) == 2:
                stats[row[0]] = row[1]

    return stats


def parse_prokka_genes(work_dir, sample_id):
    """
    Reads the Prokka .tsv file and returns a dict of named genes like:
    { "abgT": "p-aminobenzoyl-glutamate transport protein", "gyrA": "DNA gyrase subunit A" }

    Genes without a name (hypothetical proteins) are skipped
    because they are not useful for biological comparison.

    Returns None if the file is not found.
    """
    prokka_tsv = os.path.join(work_dir, "Prokka", sample_id, f"{sample_id}.tsv")

    if not os.path.exists(prokka_tsv):
        return None

    genes = {}
    with open(prokka_tsv, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            gene_name = row.get("gene", "").strip()
            product = row.get("product", "").strip()
            # only keep rows that have an actual gene name
            if gene_name:
                genes[gene_name] = product

    return genes


def comparison(request):
    """
    Shows all completed runs as checkboxes.
    When the user submits:
    - parses QUAST stats and shows a side-by-side assembly quality table
    - parses Prokka gene annotations and shows which genes are shared,
      unique to run A, or unique to run B
    """

    all_runs = PipelineRun.objects.filter(status="DONE").order_by("-created_at")

    comparison_data = []
    selected_ids = request.GET.getlist("runs")

    # this will hold the gene comparison result across all selected runs
    gene_comparison = None

    if selected_ids:
        selected_runs = PipelineRun.objects.filter(id__in=selected_ids, status="DONE")

        for run in selected_runs:
            sample_id = f"sample_{run.id}"
            quast_stats = parse_quast_report(run.work_dir)
            prokka_genes = parse_prokka_genes(run.work_dir, sample_id)

            comparison_data.append({
                "run": run,
                "quast": quast_stats,
                "prokka_genes": prokka_genes,
            })

        # gene comparison only makes sense when exactly 2 runs are selected
        # for more runs you would need a proper pan-genome tool like Roary
        if len(comparison_data) == 2:
            genes_a = set(comparison_data[0]["prokka_genes"].keys()) if comparison_data[0]["prokka_genes"] else set()
            genes_b = set(comparison_data[1]["prokka_genes"].keys()) if comparison_data[1]["prokka_genes"] else set()

            shared = genes_a & genes_b
            only_in_a = genes_a - genes_b
            only_in_b = genes_b - genes_a

            gene_comparison = {
                "run_a": comparison_data[0]["run"],
                "run_b": comparison_data[1]["run"],

                # shared genes - just the names sorted alphabetically
                "shared": sorted(shared),

                # unique genes - include the product description so the biologist
                # knows what the gene actually does
                "only_in_a": sorted([
                    {"gene": g, "product": comparison_data[0]["prokka_genes"][g]}
                    for g in only_in_a
                ], key=lambda x: x["gene"]),

                "only_in_b": sorted([
                    {"gene": g, "product": comparison_data[1]["prokka_genes"][g]}
                    for g in only_in_b
                ], key=lambda x: x["gene"]),

                "shared_count": len(shared),
                "only_in_a_count": len(only_in_a),
                "only_in_b_count": len(only_in_b),
            }

    quast_metrics = [
        "Total length",
        "# contigs",
        "N50",
        "N90",
        "GC (%)",
        "Largest contig",
    ]

    return render(request, "execution/comparison.html", {
        "all_runs": all_runs,
        "comparison_data": comparison_data,
        "selected_ids": selected_ids,
        "quast_metrics": quast_metrics,
        "gene_comparison": gene_comparison,
    })