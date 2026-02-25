def build_nextflow_params(run):
    """
    Convert user answers (stored in run.parameters)
    into actual Nextflow parameters dictionary.
    """

    user_params = run.parameters or {}
    nf_params = {}

    # -------------------------
    # Sequencing Type
    # -------------------------
    if run.sequencing_type == "PE":
        nf_params["assembly_type"] = "short"
        nf_params["assembler"] = "spades"

    elif run.sequencing_type == "LR":
        nf_params["assembly_type"] = "long"
        nf_params["assembler"] = "canu"

    elif run.sequencing_type == "HY":
        nf_params["assembly_type"] = "hybrid"
        nf_params["assembler"] = "unicycler"

    # -------------------------
    # Optional Parameters
    # -------------------------
    if not user_params.get("contamination", False):
        nf_params["skip_kraken2"] = True
        nf_params["skip_kmerfinder"] = True

    if not user_params.get("annotation", False):
        nf_params["skip_annotation"] = True
    else:
        nf_params["annotation_tool"] = user_params.get("annotation_tool", "prokka")

    if not user_params.get("busco", False):
        nf_params["skip_busco"] = True
    else:
        nf_params["busco_lineage"] = "bacteria_odb10"

    return nf_params