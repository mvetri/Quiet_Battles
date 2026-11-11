
from django.shortcuts import render, redirect
from products.models import Product
from .forms import ContactForm


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'home.html', {
        'contact_form': form
    })


def shop(request):
    products = Product.objects.filter(is_active=True)

    return render(request, 'shop.html', {
        'products': products
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form
    })


def contact_success(request):
    return render(request, 'contact_success.html')
