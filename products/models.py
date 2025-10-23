from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(unique=True)
    category_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['category_name']

    def get_url(self):
        return reverse('products:product_category', args=[self.category_slug])


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='products/', blank=True, null=True)
    parts = models.TextField(null=True, blank=True)
    parts_description = models.CharField(max_length=255, blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-created_at']

    def get_url(self):
        return reverse('products:product_detail', args=[self.category.category_slug, self.product_slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.product_name}"

class slider(models.Model):
    title_slider = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='slider/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicon/', blank=True, null=True)

    def __str__(self):
        return self.title_slider
        