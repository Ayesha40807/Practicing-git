from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
register=template.Library()
def currency_euro(value):
    return f" ₹{value:.2f}"

def productimage(value):
    return static(f'image/{value}')

register.filter('currency_euro',currency_euro)
register.simple_tag(productimage)