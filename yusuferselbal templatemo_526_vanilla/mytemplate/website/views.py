from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from .models import Service, Category
from .forms import ContactForm

# Create your views here.
def home(request): #Home Page
    return render(request, "website/home.html")

def info(request): #Info Page
    return render(request, "website/info.html")

def our_story(request): #Our Story Page
    return render(request, "website/our-story.html")

def contact_us(request): #Contact Us Page
    if request.method == 'POST':
        contactForm = ContactForm(request.POST)
        if contactForm.is_valid():
            subject = "Contact Us Message"
            body = {
                'name': contactForm.cleaned_data['name'],
                'email': contactForm.cleaned_data['email'],
                'message':  contactForm.cleaned_data['message'],
            }
            message = '\n'.join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com']) #Test E-Mail Address
            except BadHeaderError:
                return render(request, 'website/contact-us-invalid-header.html')
            
    contactForm = ContactForm()
    return render(request, 'website/contact-us.html', {
        'form': contactForm,
     })

def services(request): #Services Page
    service = Service.objects.all()
    return render(request, "website/services.html", {
        'services': service,
    })

def serviceDetail(request, slug): #Service Detail Page
    service = get_object_or_404(Service, slug = slug, is_active = True)
    return render(request, 'website/service-detail.html', {
        'service': service,
    })

def categoryFilter(request, category_slug): #Services: Category Filter
    selected = get_object_or_404(Category, slug = category_slug)
    service = Service.objects.filter(category = selected)
    return render(request, 'website/service-category.html', {
        'category': selected, 
        'service': service,
    })