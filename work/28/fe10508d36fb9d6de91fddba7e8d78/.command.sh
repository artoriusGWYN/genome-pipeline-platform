#!/usr/bin/env bash -C -e -u -o pipefail
unicycler \
    --threads 4 \
     \
    -1 ERR064912_1.fastp.fastq.gz -2 ERR064912_2.fastp.fastq.gz \
     \
    --out ./

mv assembly.fasta ERR064912.scaffolds.fa
gzip -n ERR064912.scaffolds.fa
mv assembly.gfa ERR064912.assembly.gfa
gzip -n ERR064912.assembly.gfa
mv unicycler.log ERR064912.unicycler.log

cat <<-END_VERSIONS > versions.yml
"NFCORE_BACASS:BACASS:UNICYCLER":
    unicycler: $(echo $(unicycler --version 2>&1) | sed 's/^.*Unicycler v//; s/ .*$//')
END_VERSIONS
