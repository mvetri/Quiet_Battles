
# from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from decimal import Decimal
from .models import Order, OrderItem, Product

# def product_detail(request):
#     return render(request, 'product.html')
def product_detail(request):
    products = Product.objects.filter(is_active=True)

    return render(request, 'product.html', {
        'products': products,
    })

def product_detail_page(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True
    )

    return render(request, 'product_detail.html', {
        'product': product,
    })


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))

        if size not in ['S', 'M', 'L', 'XL'] or quantity < 1:
            return redirect('shop')

        product = get_object_or_404(
            Product,
            id=product_id,
            is_active=True
        )

        cart = request.session.get('cart', {})

        cart_key = f"{product.id}_{size}"

        cart[cart_key] = cart.get(cart_key, 0) + quantity

        request.session['cart'] = cart

    return redirect('cart')




def cart(request):
    cart_items = request.session.get('cart', {})

    items = []
    total = Decimal('0.00')

    for cart_key, quantity in cart_items.items():

        try:
            product_id, size = cart_key.rsplit('_', 1)

            product = Product.objects.get(
                id=int(product_id),
                is_active=True
            )

        except (ValueError, Product.DoesNotExist):
            continue

        price = product.price
        subtotal = price * quantity
        total += subtotal

        items.append({
            'cart_key': cart_key,
            'product': product,
            'name': product.name,
            'size': size,
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'items': items,
        'total': total,
    })


def remove_from_cart(request, cart_key):
    if request.method == 'POST':
        cart_items = request.session.get('cart', {})

        cart_items.pop(cart_key, None)

        request.session['cart'] = cart_items

    return redirect('cart')


def checkout(request):
    cart_items = request.session.get('cart', {})

    if not cart_items:
        return redirect('cart')

    items = []
    total = Decimal('0.00')

    for cart_key, quantity in cart_items.items():
        try:
            product_id, size = cart_key.rsplit('_', 1)
            product = Product.objects.get(
                id=int(product_id),
                is_active=True
            )
        except (ValueError, Product.DoesNotExist):
            continue

        price = product.price
        subtotal = price * quantity
        total += subtotal

        items.append({
            'product': product,
            'name': product.name,
            'size': size,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal,
        })

    if not items:
        return redirect('cart')

    return render(request, 'checkout.html', {
        'items': items,
        'total': total,
    })


    
def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    cart_items = request.session.get('cart', {})

    if not cart_items:
        return redirect('cart')

    name = request.POST.get('customer_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()

    if not all([name, email, phone, address]):
        return redirect('checkout')

    order_products = []
    total = Decimal('0.00')

    for cart_key, quantity in cart_items.items():
        try:
            product_id, size = cart_key.rsplit('_', 1)

            product = Product.objects.get(
                id=int(product_id),
                is_active=True
            )

            if size not in ['S', 'M', 'L', 'XL'] or quantity < 1:
                continue

        except (ValueError, Product.DoesNotExist):
            continue

        price = product.price
        subtotal = price * quantity
        total += subtotal

        order_products.append({
            'product': product,
            'size': size,
            'quantity': quantity,
            'price': price,
        })

    if not order_products:
        return redirect('cart')

    order = Order.objects.create(
        customer_name=name,
        email=email,
        phone=phone,
        address=address,
        total_amount=total,
    )

    for item in order_products:
        OrderItem.objects.create(
            order=order,
            product_name=item['product'].name,
            size=item['size'],
            quantity=item['quantity'],
            price=item['price'],
        )

    request.session['cart'] = {}

    return redirect('order_success', order_id=order.id)



def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'order_success.html', {
        'order': order,
    })