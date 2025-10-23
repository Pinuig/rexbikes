from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('download_invoice/<str:order_number>/', views.download_invoice, name='download_invoice'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]