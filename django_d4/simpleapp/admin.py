from django.contrib import admin
from .models import Category, Product


def nullfy_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)
    nullfy_quantity.short_description = 'Обнулить товары'


class ProductAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Product._meta.get_fields()]
    list_display = ('name', 'price', 'quantity', 'on_stock')
    list_filter = ('price', 'quantity', 'name')
    search_fields = ('name', 'category__name')
    actions = [nullfy_quantity]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
# admin.site.unregister(Product)  # разрегистрируем наши товары
