from django import template
from test_app.models import MenuItem
from django.urls import resolve

register = template.Library()

def get_active_menu_item(request, menu_name):
    try:
        return MenuItem.objects.filter(menu_name=menu_name).get(url=request.path)
    except MenuItem.DoesNotExist:
        return None

def build_menu(menu_items, active_item):
    menu_dict = {}
    for item in menu_items:
        if item.parent is None:
            menu_dict[item] = []
    
    for item in menu_items:
        if item.parent is not None:
            menu_dict[item.parent].append(item)

    return menu_dict

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    menu_items = MenuItem.objects.filter(menu_name=menu_name)
    active_item = get_active_menu_item(request, menu_name)
    menu_dict = build_menu(menu_items, active_item)

    def render_menu(items, level=0):
        html = '<ul class="level-{}">'.format(level)
        for item in items:
            is_active = item == active_item or (active_item and item in active_item.get_ancestors())
            html += '<li class="{}">'.format('active' if is_active else '')
            html += '<a href="{}">{}</a>'.format(item.get_absolute_url(), item.name)
            if item in menu_dict:
                html += render_menu(menu_dict[item], level + 1)
            html += '</li>'
        html += '</ul>'
        return html

    return render_menu(menu_dict.keys())