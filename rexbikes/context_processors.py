from products.models import slider

def slider_links(request):
    slide = slider.objects.first()
    return dict(slide=slide)