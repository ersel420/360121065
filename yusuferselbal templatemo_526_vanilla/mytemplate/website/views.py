from http.client import HTTPResponse
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
# Main Pages
def home(request):
    return render(request, "website/home.html")

def services(request):
    return render(request, "website/services.html")

def portfolio(request):
    return render(request, "website/portfolio.html")

def our_story(request):
    return render(request, "website/our-story.html")

def contact_us(request):
    return render(request, "website/contact-us.html")

