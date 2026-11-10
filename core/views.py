from django.shortcuts import render
from products.models import Product


def home(request):
    return render(request, 'home.html')


def shop(request):
    products = Product.objects.filter(is_active=True)

    return render(request, 'shop.html', {
        'products': products
    })