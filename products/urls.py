
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_detail, name='product_detail'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    # path('remove/<str:size>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove/<str:cart_key>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('<slug:slug>/', views.product_detail_page, name='product_detail_page'),
]
