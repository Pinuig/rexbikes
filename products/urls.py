from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('category/<slug:category_slug>/', views.shop, name='product_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
]

