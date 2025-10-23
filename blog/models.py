from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Blog(models.Model):
    blog_name = models.CharField(max_length=200, unique=True)
    blog_slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(max_length=5000)
    blog_image = models.ImageField(upload_to='blogs/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.blog_name
    
    class Meta:
        managed = True
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
    
    def get_url(self):
        return reverse('blog:blog', args=[self.blog_slug])