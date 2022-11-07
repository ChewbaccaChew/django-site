from django import template

from women.models import *

register = template.Library()


@register.simple_tag(name='getcats')  # теперь вызов функции через getcats вместо get_categories
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()  # использовать в шаблоне можно так: {% getcats as categories %} и уже categories перебирать
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('women/list_categories.html')  # результат передается указанному шаблону list_categories.html
# использовать в конечном шаблоне можно так: {% show_categories '-name' cat_selected %}
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}  # результат

