from django.contrib import admin
from .models import Blog
# Register your models here.

class blogAdmin(admin.ModelAdmin):
    list_display = ('blog_name', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    prepopulated_fields = {'blog_slug': ('blog_name',)}
    search_fields = ('blog_name', 'author')
    ordering = ('blog_name', '-created_at')

admin.site.register(Blog, blogAdmin)