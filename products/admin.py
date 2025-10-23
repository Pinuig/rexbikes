from django.contrib import admin
from .models import Category, Product, ProductImage, slider
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_slug')
    search_fields = ('category_name',)
    prepopulated_fields = {'category_slug': ('category_name',)}
admin.site.register(Category, CategoryAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'created_at', 'updated_at')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'product_slug': ('product_name',)}
    search_fields = ('product_name', 'description')
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(slider)
