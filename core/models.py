from django.db import models

# Create your models here.
class contact(models.Model):
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact_name
    

class newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class AboutUs(models.Model):
    about_title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    about_image = models.ImageField(upload_to='media/about/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.about_title
    
class socials(models.Model):
    links = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.links