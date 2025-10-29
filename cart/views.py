from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartItem, Cart, Order, OrderItem, Coupon
import datetime
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import F
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart:cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart:cart')

def cart(request, total=0, quantity=0, cart_items=None):
    subtotal = Decimal('0.00')
    quantity = 0
    shipping_charge = Decimal('0.00')
    grand_total = Decimal('0.00')
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            grand_total = total 
            if subtotal <= 500:
                shipping_charge = Decimal('10.00')
        
            grand_total = subtotal + shipping_charge
    except Cart.DoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
    }
    return render(request, 'cart/cart.html', context)

# cart/views.py

def checkout(request):
    total = Decimal('0.00')
    quantity = 0
    shipping_charge = Decimal('0.00')
    grand_total = Decimal('0.00')
    cart_items = None
    discount_amount = Decimal('0.00')
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
    except Cart.DoesNotExist:
        pass

    if total > 0 and total <= 500:
        shipping_charge = Decimal('153.83')
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            discount_amount = (Decimal(coupon.discount) / 100) * total
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None) 
    grand_total = (total - discount_amount) + shipping_charge
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping_charge': shipping_charge,
        'discount_amount': discount_amount, 
        'grand_total': grand_total,      
    }
    return render(request, 'cart/checkout.html', context)



# cart/views.py

def place_order(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    if not cart_items.exists():
        return redirect('products:shop')

    if request.method != 'POST':
        return redirect('cart:checkout')

    total = Decimal('0.00')
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)

    shipping_charge = Decimal('0.00')
    if total <= Decimal('500'):
        shipping_charge = Decimal('157.83')

    grand_total_before_coupon = total + shipping_charge
    discount_amount = Decimal('0.00')
    final_grand_total = grand_total_before_coupon
    
    coupon_id = request.session.get('coupon_id')
    coupon = None
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            discount_amount = (Decimal(coupon.discount) / 100) * total
            final_grand_total = (total - discount_amount) + shipping_charge
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)
            pass 

    try:
        with transaction.atomic():
            order = Order()
            # FIX: The field `order.total` should store the subtotal, not the total with shipping.
            order.total = total 
            order.shipping_charge = shipping_charge
            order.discount = discount_amount
            order.order_total = final_grand_total
            order.ip = request.META.get('REMOTE_ADDR')
            
            
            order.billing_first_name = request.POST.get('billing_first_name')
            order.billing_last_name = request.POST.get('billing_last_name')
            order.billing_address = request.POST.get('billing_address')
            order.billing_city = request.POST.get('billing_city')
            order.billing_email = request.POST.get('billing_email')
            order.billing_phone = request.POST.get('billing_phone')
            order.shipping_first_name = request.POST.get('shipping_first_name')
            order.shipping_last_name = request.POST.get('shipping_last_name')
            order.shipping_address = request.POST.get('shipping_address')
            order.shipping_city = request.POST.get('shipping_city')
            order.shipping_email = request.POST.get('shipping_email')
            order.shipping_phone = request.POST.get('shipping_phone')
            order.payment_method = request.POST.get('payment_method')
            order.order_note = request.POST.get('message')
            order.save()
            
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            order.order_number = f"{yr}{mt:02d}{order.id}" 
            order.save() 
            
            order_i = OrderItem.objects.filter(order=order)

            try:
                mail_subject = f'Your Rex Bikes Order Confirmation - #{order.order_number}'
                email_context = {
                    'order': order,
                    'order_i': order_i,
                }
                html_message = render_to_string('cart/order_confirmation_customer.html', email_context)
                plain_message = render_to_string('cart/order_confirmation_customer.txt', email_context)

                send_mail(
                    subject=mail_subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.billing_email],
                    html_message=html_message,
                    fail_silently=False, 
                )
            except Exception as e:
                print(f"Customer confirmation email failed for order {order.order_number}: {e}")

            

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                    ordered=True
                )

           
            if coupon:
                coupon.used = F('used') + 1
                coupon.save()
                request.session.pop('coupon_id', None)
            
           
            cart_items.delete()

            order_items = OrderItem.objects.filter(order=order)
            context = { 
                'order': order, 
                'order_items': order_items, 
                'order_i': order_i,
                'grand_total_before_coupon': grand_total_before_coupon, 
            }
            return render(request, 'cart/order.html', context) 

    except Exception as e:
        messages.error(request, f'There was an error processing your order: {e}. Please try again.')
        return redirect('cart:checkout')

def download_invoice(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        order_items = OrderItem.objects.filter(order=order)
    except Order.DoesNotExist:
        # You can return a 404 page or a simple message
        return HttpResponse("Invoice not found.", status=404)
    
   
    
    # grand_total_before_coupon = order.total + order.shipping_charge
    grand_total_before_coupon = order.order_total

    # for item in order_items:
    #     item.total = item.quantity * item.product.price

    for item in order_items:
        item._computed_total = Decimal(item.quantity) * Decimal(item.product.price)


    context = {
        'order': order,
        'order_items': order_items,
        'grand_total_before_coupon': grand_total_before_coupon,
    }

    html_string = render_to_string('cart/order.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice-{order.order_number}.pdf"'

    return response

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        now = timezone.now()
        
        try:
            coupon = Coupon.objects.get(
                code__iexact=coupon_code, 
                is_active=True,
                valid_from__lte=now,
                valid_to__gte=now,
                used__lt=F('max_uses')
            )
            request.session['coupon_id'] = coupon.id
            return JsonResponse({'status': 'success', 'message': 'Coupon applied successfully!'})
        
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)
            return JsonResponse({'status': 'error', 'message': 'Invalid, expired, or fully used coupon code.'})
    
    return redirect('cart:checkout')