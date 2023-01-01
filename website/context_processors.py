from .models import Category

def categories(request): #Get all Categories
    return {
        'categories': Category.objects.all() 
    }