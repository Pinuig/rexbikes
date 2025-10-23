from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('contact/', views.contact_view, name='contact_view'), 
    path('about/', views.about_us_view, name='about_us_view'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('shipping_policy/', views.shipping_policy, name='shipping_policy'),
    path('terms/', views.terms, name='terms'),
    path('faq/', views.faq, name='faq'),
    path('return_policy/', views.return_policy, name='return_policy'),
]
