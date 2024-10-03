from django.shortcuts import render

# Create your views here.
from django import template
from django.urls import reverse, NoReverseMatch
from .models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu.html')
def draw_menu(menu_name):
    menu_items = MenuItem.objects.filter(menu_name=menu_name).order_by('parent__id', 'id')
    return {'menu_items': menu_items}