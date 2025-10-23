from django.contrib import admin
from .models import contact, newsletter, AboutUs, socials
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'email', 'created_at')
    search_fields = ('contact_name', 'email')
    readonly_fields = ('contact_name', 'email', 'message', 'created_at')
    ordering = ('-created_at',)

admin.site.register(contact, ContactAdmin)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('email', 'subscribed_at')
    ordering = ('-subscribed_at',)

admin.site.register(newsletter, NewsletterAdmin)

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('about_title', 'created_at', 'updated_at')
    search_fields = ('about_title',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(AboutUs, AboutUsAdmin)

class SocialsAdmin(admin.ModelAdmin):
    list_display = ('links',)
    search_fields = ('links',)  

admin.site.register(socials, SocialsAdmin)
