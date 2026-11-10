
from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'is_active',
        'created_at',
    )

    list_filter = ('is_active',)

    search_fields = ('name', 'description')

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_editable = ('is_active',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'email',
        'phone',
        'total_amount',
        'created_at',
    )

    search_fields = ('customer_name', 'email', 'phone')

    list_filter = ('created_at',)

    inlines = [OrderItemInline]


admin.site.register(OrderItem)
