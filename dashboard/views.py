
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Sum, Q

from products.models import Product, Order
from .forms import ProductForm
from core.models import ContactMessage

# Staff-only dashboard protection
def staff_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url='/admin/login/'
    )(view_func)


@staff_required
def dashboard_home(request):

    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()

    total_messages = ContactMessage.objects.count()

    total_revenue = Order.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_customers = Order.objects.values('email').distinct().count()

    recent_orders = Order.objects.order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'total_messages': total_messages,
        'recent_orders': recent_orders,
    }

    return render(request, 'dashboard/dashboard.html', context)

@staff_required
def product_list(request):

    search = request.GET.get('search', '')
    products = Product.objects.all().order_by('-created_at')

    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'dashboard/product_list.html', {
        'products': products,
        'search': search,
    })


@staff_required
def product_add(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': 'Add Product',
    })


@staff_required
def product_edit(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': 'Edit Product',
    })


@staff_required
@require_POST
def product_delete(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    product.delete()

    messages.success(request, 'Product deleted successfully!')

    return redirect('product_list')


@staff_required
def order_list(request):

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    orders = Order.objects.prefetch_related('items').order_by('-created_at')

    # Search by order ID, customer name, or email
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(customer_name__icontains=search) |
            Q(email__icontains=search)
        )

    # Filter by order status
    if status:
        orders = orders.filter(status=status)

    context = {
        'orders': orders,
        'search': search,
        'selected_status': status,
        'status_choices': Order.STATUS_CHOICES,
    }

    return render(request, 'dashboard/order_list.html', context)


@staff_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        id=order_id
    )

    if request.method == 'POST':
        new_status = request.POST.get('status')

        valid_statuses = [
            choice[0] for choice in Order.STATUS_CHOICES
        ]

        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully!')
            return redirect('order_detail', order_id=order.id)

    order_items = order.items.all()

    for item in order_items:
        item.subtotal = item.price * item.quantity

    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'order_items': order_items,
        'status_choices': Order.STATUS_CHOICES,
    })


@staff_required
def contact_message_list(request):

    search = request.GET.get('search', '').strip()

    contact_messages = ContactMessage.objects.all().order_by('-created_at')

    if search:
        contact_messages = contact_messages.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(subject__icontains=search) |
            Q(message__icontains=search)
        )

    return render(request, 'dashboard/contact_messages.html', {
        'contact_messages': contact_messages,
        'search': search,
    })


@staff_required
def contact_message_detail(request, message_id):
    contact_message = get_object_or_404(ContactMessage, id=message_id)

    if not contact_message.is_read:
        contact_message.is_read = True
        contact_message.save()

    return render(request, 'dashboard/contact_message_detail.html', {
        'contact_message': contact_message,
    })