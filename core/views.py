from django.shortcuts import render
from django import forms
from django.http import HttpResponse

#views that belongs to the core app

# Create your views here.

class guidanceFrom(forms.Form):

    
    inputData = [
        ("fastq", "RAW sequencing reads (FASTQ)"),
        ("fasta", "One assembled genome (FASTA)"),
        ("multi_fasta", "Several assembled genomes"),
        ("unknown", "I don't know"),
    ]

    organismNumber = [
        ("one", "One organism"),
        ("multiple", "Multiple organisms"),
        ("unknown", "Unknown / Mixed community"),
    ]

    biologicalGoal = [
        ("annotation", "Gene annotation & functions"),
        ("compare", "Compare genomes / find shared genes"),
        ("taxonomy", "Identify species and metabolic potential"),
        ("unsure", "Not sure"),
    ]

    organismType = [
        ("bacteria", "Bacteria / archaea"),
        ("mixed", "Mixed environmental sample"),
        ("unknown", "Not sure"),
    ]
    
    
    dataInfo = forms.ChoiceField(choices=inputData, 
                                 widget=forms.RadioSelect, 
                                 label="What kind of data do you have")
    
    numberInfo = forms.ChoiceField(choices=organismNumber, 
                                   widget=forms.RadioSelect, 
                                   label="does your data come from:")
    
    goalInfo = forms.ChoiceField(choices=biologicalGoal, 
                                 widget=forms.RadioSelect, 
                                 label="What do you want to obtain")
    
    typeInfo = forms.ChoiceField(choices=organismType, 
                                 widget=forms.RadioSelect, 
                                 label="What best describes your data ")
    

    


def home(request):
    return render(request, "core/home.html")

def guidance(request): 
    if request.method == 'POST':
        form = guidanceFrom(request.POST)
        if form.is_valid():
            return HttpResponse("here we will execute the logic that chooses the pipeline for the user")
    else:
            form = guidanceFrom()
            
    return render(request, "core/pipeline_guidance.html", {
        "guidance_data" : form 
    })






