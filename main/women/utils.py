from django.db.models import Count
from django.core.cache import cache  # API низкого уровня для кэширования

from .models import *

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]


class DataMixin:
    paginate_by = 3  # встроенный в ListView атрибут, принимает количество элементов на одной странице

    def get_user_context(self, **kwargs):
        context = kwargs  # формируем словарь из именованных параметров переданных функции get_user_context

        # cats = cache.get('cats')  # выбор данных из кэша по ключу
        # if not cats:  # если cats хранит None, то есть данные не были прочитаны
        #     cats = Category.objects.annotate(Count('women'))  # то читаем данные из таблицы
        #     cache.set('cats', cats, 60)  # и сохраняем их по ключу с указанием времени использования в секундах

        # cats = Category.objects.all()  # список категорий; чтобы пустые категории не отображались:
        cats = Category.objects.annotate(Count('women'))  # создаем список всех рубрик с атрибутом women__count для каждой,
        # который содержит количество связанных с ней(рубрикой) записей

        # чтобы пункт 'Добавить статью' отображался только для авторизованных
        # вместо:
        # context['menu'] = menu
        # сделаем проверку:
        user_menu = menu.copy()  # копия словаря menu
        if not self.request.user.is_authenticated:  # если пользователь не авторизован
            user_menu.pop(1)  # удалить второй пункт(Добавить статью) из копии menu
        context['menu'] = user_menu  # передаем в контекст измененное меню

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
