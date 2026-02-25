from celery import shared_task
from .models import PipelineRun
from .utils import build_nextflow_params
import subprocess
import os
import json
from django.utils import timezone
import logging
import shlex

logger = logging.getLogger(__name__)

@shared_task
def run_pipeline(run_id):
    run = PipelineRun.objects.get(id=run_id)

    try:
        run.status = "RUNNING"
        run.started_at = timezone.now()
        run.save()

        # Create output directory
        outdir = os.path.abspath(os.path.join("runs", str(run.id)))
        os.makedirs(outdir, exist_ok=True)
        run.work_dir = outdir
        run.save()

        # Build Nextflow parameters
        nf_params = build_nextflow_params(run)

        # Input handling: prefer samplesheet
        if run.samplesheet:
            input_path = os.path.abspath(run.samplesheet.path)
            nf_params["input"] = input_path
        else:
            # Build pseudo-samplesheet if user uploaded individual files
            if run.fastq_r1 and run.fastq_r2 or run.nanopore:
                # This is an example, you may need to adapt based on pipeline spec
                nf_params["fastq_r1"] = os.path.abspath(run.fastq_r1.path) if run.fastq_r1 else "NA"
                nf_params["fastq_r2"] = os.path.abspath(run.fastq_r2.path) if run.fastq_r2 else "NA"
                nf_params["nanopore"] = os.path.abspath(run.nanopore.path) if run.nanopore else "NA"
            else:
                raise ValueError("No input files provided for pipeline")

        nf_params["outdir"] = outdir

        # Write params.json
        params_file_path = os.path.join(outdir, "params.json")
        with open(params_file_path, "w") as f:
            json.dump(nf_params, f, indent=4)

        # Nextflow command
        nf_command = [
            "nextflow", "run", "nf-core/bacass",
            "-r", "2.5.0",
            "-profile", "docker",
            "--outdir", outdir,
            "--params-file", params_file_path
        ]
        if "input" in nf_params:
            nf_command += ["--input", nf_params["input"]]

        logger.info("Running Nextflow command: %s", shlex.join(nf_command))

        # Run Nextflow
        result = subprocess.run(
            nf_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Save logs
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