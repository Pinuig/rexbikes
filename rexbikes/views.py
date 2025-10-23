from django.shortcuts import render
from products.models import Product, slider, Category
from blog.models import Blog

def index(request):
    product = Product.objects.all().filter(available=True)
    slide = slider.objects.first()
    recent_product = Product.objects.order_by('-created_at')[:6]
    post = Blog.objects.all().order_by('-created_at')

    try:
        category = Category.objects.get(category_name='Frames & Fork, clothes',)
        others = Product.objects.filter(category=category)
    except Category.DoesNotExist:
        others = Product.objects.none()
    context = {
        'product': product,
        'slide': slide,
        'recent_product': recent_product,
        'others': others,
        'post': post
    }
    return render(request, 'index.html', context)


