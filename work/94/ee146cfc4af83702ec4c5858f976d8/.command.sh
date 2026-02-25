#!/usr/bin/env bash -C -e -u -o pipefail
printf "%s %s\n" ERR064912_1.fastp.fastq.gz ERR064912_1.gz ERR064912_2.fastp.fastq.gz ERR064912_2.gz | while read old_name new_name; do
    [ -f "${new_name}" ] || ln -s $old_name $new_name
done

fastqc \
    --quiet \
    --threads 4 \
    --memory 3840 \
    ERR064912_1.gz ERR064912_2.gz

cat <<-END_VERSIONS > versions.yml
"NFCORE_BACASS:BACASS:FASTQ_TRIM_FASTP_FASTQC:FASTQC_TRIM":
    fastqc: $( fastqc --version | sed '/FastQC v/!d; s/.*v//' )
END_VERSIONS
