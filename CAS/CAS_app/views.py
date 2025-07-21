from django.shortcuts import render

# Create your views here.

def home_view(request):
    return render(request, "website/home.html")

def resume_advisor_view(request):
    return render(request, "website/resume_advisor.html")