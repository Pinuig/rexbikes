from django.shortcuts import render, get_object_or_404, Http404
from .models import Product, Category, ProductImage
from cart.models import CartItem
from cart.views import _cart_id
from django.db.models import Q

# Create your views here.
def shop(request, category_slug=None):
    categories = None
    product = None
    recent_products = Product.objects.none()

    if category_slug != None:
        categories = get_object_or_404(Category, category_slug=category_slug)
        product = Product.objects.filter(category=categories, available=True)
    else:
        product = Product.objects.all().filter(available=True)
        recent_products = Product.objects.order_by('-created_at')[:4]
        
        # product_count = product.count()

    context = {
        'categories': categories,
        'product': product,
        # 'product_count': product_count,
        'recent_products': recent_products,
       
    }
    return render(request, 'shop/shop.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__category_slug=category_slug, product_slug=product_slug)
        images = ProductImage.objects.filter(product=single_product)
        related_products = Product.objects.filter(category=single_product.category).exclude(id=single_product.id)[:4]
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    except Exception as e:
        raise e
    
    
    context = {
        'single_product': single_product,
        'images': images,
        'related_products': related_products,
        'in_cart': in_cart,
    }
    return render(request, 'shop/product_details.html', context)


def search(request):
    producted = Product.objects.none() 
    keyword = request.GET.get('keyword', '')


    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            search_query = Q(product_name__icontains=keyword) | Q(description__icontains=keyword)
            producted = Product.objects.filter(search_query).order_by('-created_at').distinct()

    context = {
            'producted': producted,
            'keyword': keyword,
        }
    return render(request, 'shop/shop.html', context)

