from django.shortcuts import render
from .models import contact, newsletter, AboutUs, socials

# Create your views here.
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact.objects.create(contact_name=name, email=email, message=message)
        return render(request, 'core/contact.html', {'success': True})
    return render(request, 'core/contact.html')

def about_us_view(request):
    about_info = AboutUs.objects.all()
    return render(request, 'core/about.html', {'about_info': about_info})



def socials_view(request):
    social_links = socials.objects.all()
    return render(request, 'core/socials.html', {'social_links': social_links})

def newsletter_subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not newsletter.objects.filter(email=email).exists():
            newsletter.objects.create(email=email)
            return render(request, 'core/newsletter_subscribe.html', {'subscribed': True})
        else:
            return render(request, 'core/newsletter_subscribe.html', {'already_subscribed': True})
    return render(request, 'core/newsletter_subscribe.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def terms(request):
    return render(request, 'core/terms.html')

def shipping_policy(request):
    return render(request, 'core/shipping_policy.html')

def faq(request):
    return render(request, 'core/faq.html')

def return_policy(request):
    return render(request, 'core/return.html')

