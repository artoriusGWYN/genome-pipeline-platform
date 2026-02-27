import os
import csv
import json
import subprocess
import shlex
import logging
from django.utils import timezone
from celery import shared_task
from .models import PipelineRun
from .utils import build_nextflow_params

logger = logging.getLogger(__name__)


@shared_task
def run_pipeline(run_id):

    run = PipelineRun.objects.get(id=run_id)

    try:
        run.status = "RUNNING"
        run.started_at = timezone.now()
        run.save()

        # creating output directory
        outdir = os.path.abspath(os.path.join("runs", str(run.id)))
        os.makedirs(outdir, exist_ok=True)

        run.work_dir = outdir
        run.save()

        # generation of a tsv file that complies with the bacass standards in case the user upaloads fastq files 
        if run.samplesheet:
            samplesheet_path = os.path.abspath(run.samplesheet.path)

        else:
            if not (run.fastq_r1 or run.nanopore):
                raise ValueError("No input files provided.")

            samplesheet_path = os.path.join(outdir, "samplesheet.tsv")

            with open(samplesheet_path, "w", newline="") as tsv:
                writer = csv.writer(tsv, delimiter="\t")

                writer.writerow([
                    "ID",
                    "R1",
                    "R2",
                    "LongFastQ",
                    "Fast5",
                    "GenomeSize"
                ])

                r1 = run.fastq_r1.path if run.fastq_r1 else "NA"
                r2 = run.fastq_r2.path if run.fastq_r2 else "NA"
                longfq = run.nanopore.path if run.nanopore else "NA"

                writer.writerow([
                    f"sample_{run.id}",
                    os.path.abspath(r1) if r1 != "NA" else "NA",
                    os.path.abspath(r2) if r2 != "NA" else "NA",
                    os.path.abspath(longfq) if longfq != "NA" else "NA",
                    "NA",
                    "NA"
                ])

        # generating nextflow parameters 
        nf_params = build_nextflow_params(run)

        nf_params["input"] = samplesheet_path
        nf_params["outdir"] = outdir

        params_file = os.path.join(outdir, "params.json")

        with open(params_file, "w") as f:
            json.dump(nf_params, f, indent=4)

        #  generating the nextflow command 
        nf_command = [
            "nextflow",
            "run",
            "nf-core/bacass",
            "-r", "2.5.0",
            "-profile", "docker",
            "-params-file", params_file
        ]

        # displaying and creating the command generated (for debugging and testing the creating of the nextflow command generation)
        command_string = shlex.join(nf_command)

        logger.info("Running Nextflow command: %s", command_string)

        with open(os.path.join(outdir, "command.sh"), "w") as f:
            f.write(command_string + "\n")

    

        # nextflow command execution using subprocess 
        result = subprocess.run(
            nf_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # saving informations 
        with open(os.path.join(outdir, "stdout.log"), "w") as f:
            f.write(result.stdout)

        with open(os.path.join(outdir, "stderr.log"), "w") as f:
            f.write(result.stderr)

        run.status = "DONE" if result.returncode == 0 else "FAILED"

    except Exception as e:
        run.status = "FAILED"

        error_log_path = os.path.join(outdir, "system_error.log")
        with open(error_log_path, "w") as f:
            f.write(str(e))

    run.finished_at = timezone.now()
    run.save()

    return f"PipelineRun {run.id} finished with status {run.status}"