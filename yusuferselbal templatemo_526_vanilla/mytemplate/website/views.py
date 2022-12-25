from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Service, Category

# Create your views here.
def home(request):
    return render(request, "website/home.html")

def services(request):
    return render(request, "website/services.html")

def portfolio(request):
    service = Service.objects.all()
    return render(request, "website/portfolio.html", {'services': service})

def serviceDetail(request, slug):
    service = get_object_or_404(Service, slug = slug, is_active = True)
    return render(request, 'website/portfolio-item.html', {'service': service})

def categoryFilter(request, category_slug):
    selected = get_object_or_404(Category, slug = category_slug)
    service = Service.objects.filter(category = selected)
    return render(request, 'website/portfolio-category.html', {'category': selected, 'service': service})

def our_story(request):
    return render(request, "website/our-story.html")

def contact_us(request):
    return render(request, "website/contact-us.html")

def login(request):
    return render(request, "website/login.html")

def register(request):
    return render(request, "website/register.html")

def profile(request):
    return render(request, "website/profile.html")