from django.contrib import admin
from .models import Order, OrderItem, Product, ProductImage, Category, Comment

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'category', 'slug', 'description', 'price')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'total_price']  # поля для відображенні в адмінці замовлення
    readonly_fields = ['total_price']  
    def total_price(self, obj):
        return f"{obj.total_price:.2f} грн"  # формат для грошей
    total_price.short_description = 'Загальна вартість'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'city', 'last_name', 'first_name', 'phone', 'additional_info', 'get_order_total')
    inlines = [OrderItemInline]
    search_fields = ['user__email', 'city', 'last_name', 'first_name', 'phone']
    list_filter = ('created_at', 'city')

    def get_order_total(self, obj):
        total = sum(item.total_price for item in obj.order_items.all())
        return f"{total:.2f} грн"  # Format as currency
    get_order_total.short_description = 'Загальна вартість'

admin.site.register(Category)
admin.site.register(Comment)
