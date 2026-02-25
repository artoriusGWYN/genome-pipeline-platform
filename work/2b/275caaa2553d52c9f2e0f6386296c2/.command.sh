#!/usr/bin/env bash -C -e -u -o pipefail
cat input1/ERR044595_1M_1.fastq.gz input3/r-ERR044595_1M_1.fastq.gz > ERR044595_1.merged.fastq.gz
cat input2/ERR044595_1M_2.fastq.gz input4/r-ERR044595_1M_2.fastq.gz > ERR044595_2.merged.fastq.gz

cat <<-END_VERSIONS > versions.yml
"NFCORE_BACASS:BACASS:CAT_FASTQ_SHORT":
    cat: $(echo $(cat --version 2>&1) | sed 's/^.*coreutils) //; s/ .*$//')
END_VERSIONS
