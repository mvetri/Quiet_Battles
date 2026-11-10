from django import forms
from products.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'slug',
            'description',
            'price',
            'image',
            'is_active',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),

            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product slug'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter product description'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
        }