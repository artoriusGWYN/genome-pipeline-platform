from django import forms

class BacassRunForm(forms.Form):

    SEQ_CHOICES = [
        ("PE", "Paired-end (Illumina)"),
        ("LR", "Long-read (Nanopore)"),
        ("HY", "Hybrid (Illumina + Nanopore)"),
    ]

    sequencing_type = forms.ChoiceField(
        choices=SEQ_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    fastq_r1 = forms.FileField(required=False)
    fastq_r2 = forms.FileField(required=False)
    nanopore = forms.FileField(required=False)