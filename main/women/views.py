from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404  # render - встроенный шаблонизатор обрабатывающий шаблоны
from django.urls import reverse_lazy
# reverse_lazy создает маршрут только тогда, когда он действительно понадобится, а не в момент создания экземпляра класса, как делает reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin  # Миксин для ограничения доступа
from django.contrib.auth.decorators import login_required  # декоратор для ограничения доступа
from django.core.paginator import Paginator  # пагинатор для функций
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):  # наследуется от ListView потому что это будет список
    """Класс главной страницы сайта"""

    model = Women  # выбирает все записи из таблицы Women и отображает в виде списка
    template_name = 'women/index.html'
    # в template_name указываем какой шаблон использовать, если не указывать, то по умолчанию формируется путь к шаблону так:
    # <имя приложения>/<имя модели>_list.html, в нашем случае -> women/women_list.html
    context_object_name = 'posts'  # явно указываем имя, которое будем использовать в шаблоне для обращения к object_list
    # extra_context = {'title': 'Главная страница'}  # так можно передавать только статические(неизменяемые) данные(числа, строки и тд)

    # передача и статических и динамических данных
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получаем контекст, который уже сформирован для шаблона index.html
        # вместо этого:
        # context['menu'] = menu  # и изменяем/дополняем его
        # context['title'] = 'Главная страница'  # вместо передачи через extra_context
        # context['cat_selected'] = 0  # отображает синим цветом пункт 'Все категории'
        # используем метод Миксина:
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items()))  # создаем списки из словарей и объединяем их в новый словарь
        return context

    # отображение на главной страницы только опубликованных статей(проставлена галочка в поле is_published)
    def get_queryset(self):
        return Women.objects.filter(is_published=True)

# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)


# @login_required  # ограничивает доступ к странице для неавторизованных
def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)  # 3 элемента списка contact_list будут отображаться на каждой странице

    page_number = request.GET.get('page')  # номер текущей страницы(которая отображается)
    page_obj = paginator.get_page(page_number)  # список элементов текущей страницы

    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):  # CreateView работает с формами;
    # LoginRequiredMixin - делает класс недоступным для неавторизованных пользователей
    # (достаточно просто наследоваться от него, чтобы заработал)
    """Класс добавления нового поста"""
    form_class = AddPostForm  # поэтому здесь указываем класс формы с которой будет связан класс представления
    template_name = 'women/addpage.html'
    # если у модели нет get_absolute_url, используем:
    success_url = reverse_lazy('home')
    # атрибуту success_url присваиваем адрес маршрута перенаправления после добавления статьи
    login_url = reverse_lazy('home')  # адрес перенаправления для неавторизованных или использовать raise_exception:
    raise_exception = True  # генерирует страницу 403 - доступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # вместо этого:
        # context['menu'] = menu
        # context['title'] = 'Добавление статьи'
        # используем метод Миксина:
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))
        # лучше использовать такой return:
        # return {**context, ** c_def}

# def addpage(request):
#     # если форма была отправлена, но не прошла проверку, возвращается пользователю с заполненными полями
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)  # заполненная форма;
#         # request.FILES - список файлов, которые были переданы на сервер из формы
#         if form.is_valid():  # если проверка пройдена
#             # print(form.cleaned_data)  # отобразить в консоли очищенные данные
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     # добавляем новую запись в таблицу; **form.cleaned_data - распаковка словаря
#             #     return redirect('home')  # если добавление прошло успешно, то переходим на главную страницу
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')  # добавляем общую ошибку, которая будет отображаться
#
#             # но если форма связанна с моделью можно сделать так:
#             form.save()  # все данные переданные от формы будут сохранены в таблице Women, которая связана с формой
#             # и сообщения об ошибках будут генерироваться django автоматически
#             return redirect('home')
#
#     else:
#         form = AddPostForm()  # пустая форма
#
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse('Обратная связь')


def page_not_found(request, exception):
    # функция для отображения ненайденных страниц
    return HttpResponseNotFound('Страница не найдена')


class ShowPost(DataMixin, DetailView):
    """Класс для отображения отдельного поста"""

    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    # slug_url_kwarg - переопределение переменной для слага, которая используется в urls -> 'post/<slug:post_slug>/',
    # по умолчанию используется имя 'slug'
    # для переопределения имени переменной для id-шника используется pk_url_kwarg = (по умолчанию 'pk')
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # вместо этого:
        # context['menu'] = menu
        # context['title'] = context['post']
        # используем метод Миксина:
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)  # из модели Women получить запись с slug=post_slug или исключение 404
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    """Класс для отображения всех статей принадлежащих конкретной категории"""

    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # если в списке нет ни одной записи, то будет вызвано исключение 404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # вместо этого:
        # context['menu'] = menu
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['cat_selected'] = context['posts'][0].cat_id
        # используем метод Мискина:
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    # выбрать опубликованные записи, которые соответствуют категории по указанному слагу
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
        # через kwargs можно получить любой элемент нашего маршрута из urls, в данном случае cat_slug
        # cat__slug: обращаемся к полю slug таблицы Category, через поле cat таблицы Women, связанной с текущей записью

# def show_category(request, cat_slug):
#     posts = Women.objects.filter(slug=cat_slug)
#
#     if len(posts) == 0:
#         raise Http404
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'women/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    """Класс для регистрации пользователя"""

    # form_class = UserCreationForm  # UserCreationForm - стандартная форма django для регистрации
    form_class = RegisterUserForm  # из forms.py
    template_name = 'women/register.html'  # ссылка на используемый шаблон
    success_url = reverse_lazy('login')  # адрес перенаправления при успешной регистрации

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    # метод авторизации, вызывается при успешной проверке формы регистрации, то есть при успешной регистрации нового пользователя
    def form_valid(self, form):
        user = form.save()  # сохраняем форму в БД, то есть добавляем пользователя в БД
        login(self.request, user)  # login - стандартная функция django для авто-авторизации
        return redirect('home')


class LoginUser(DataMixin, LoginView):  # LoginView - стандартный класс представления django
    """Класс для авторизации пользователя"""

    # form_class = AuthenticationForm  # AuthenticationForm - стандартная форма авторизации django
    form_class = LoginUserForm  # из forms.py
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        # переопределяем путь перенаправления после успешной аутентификации; по дуфолту путь: /accounts/profile/
        return reverse_lazy('home')
    # или в settings.py определить константу LOGIN_REDIRECT_URL


# функция выхода
def logout_user(request):
    logout(request)  # logout - стандартная функция django
    return redirect('login')  # перенаправление после выхода
