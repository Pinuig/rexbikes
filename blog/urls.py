from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('<slug:blog_slug>/', views.blog, name='blog'),
]
