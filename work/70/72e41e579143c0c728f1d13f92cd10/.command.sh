#!/usr/bin/env bash -C -e -u -o pipefail
[ ! -f  ERR064912_1.fastq.gz ] && ln -sf ERR064912_1M_1.fastq.gz ERR064912_1.fastq.gz
[ ! -f  ERR064912_2.fastq.gz ] && ln -sf ERR064912_1M_2.fastq.gz ERR064912_2.fastq.gz
fastp \
    --in1 ERR064912_1.fastq.gz \
    --in2 ERR064912_2.fastq.gz \
    --out1 ERR064912_1.fastp.fastq.gz \
    --out2 ERR064912_2.fastp.fastq.gz \
    --json ERR064912.fastp.json \
    --html ERR064912.fastp.html \
     \
     \
     \
    --thread 4 \
    --detect_adapter_for_pe \
     \
    2>| >(tee ERR064912.fastp.log >&2)

cat <<-END_VERSIONS > versions.yml
"NFCORE_BACASS:BACASS:FASTQ_TRIM_FASTP_FASTQC:FASTP":
    fastp: $(fastp --version 2>&1 | sed -e "s/fastp //g")
END_VERSIONS
