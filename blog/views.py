from django.shortcuts import render, get_object_or_404
from .models import Blog
from products.models import Category, Product
# Create your views here.
def blog(request, blog_slug):
    posts = get_object_or_404(Blog, blog_slug=blog_slug)
    categories = Category.objects.all()
    rendered_products = Product.objects.order_by('-created_at')[:4]
    context = {
        'posts': posts,
        'categories':categories,
        'rendered_products': rendered_products,
    }
    return render(request, 'blog.html', context)