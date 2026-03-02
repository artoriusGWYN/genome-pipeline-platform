#utils.py belong to execution app 

def build_nextflow_params(run):

    params = {}

    # email
    if run.email:
        params["email"] = run.email

    # QC
    if run.skip_fastqc:
        params["skip_fastqc"] = True
    if run.skip_fastp:
        params["skip_fastp"] = True
    if run.skip_nanoplot:
        params["skip_nanoplot"] = True
    if run.skip_toulligqc:
        params["skip_toulligqc"] = True
    if run.save_trimmed:
        params["save_trimmed"] = True

    # Assembly
    params["assembler"] = run.assembler
    params["assembly_type"] = run.assembly_type

    

    params["skip_kraken2"] = True
    params["skip_kmerfinder"] = True

    # BUSCO
    params["busco_lineage"] = run.busco_lineage
    if run.skip_busco:
        params["skip_busco"] = True

    # Annotation
    params["annotation_tool"] = run.annotation_tool
    if run.skip_annotation:
        params["skip_annotation"] = True
    

    return params