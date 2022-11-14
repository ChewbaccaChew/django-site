from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')  # поля отображаемые в админке
    list_display_links = ('id', 'title')  # поля-ссылки
    search_fields = ('title', 'content')  # поля по которым будет осуществляться поиск
    list_filter = ('is_published', 'time_create')  # поля по которым возможна фильтрация
    list_editable = ('is_published',)  # поля редактируемые прямо в админке
    prepopulated_fields = {'slug': ('title',)}  # заполнять поле slug на основе поля title
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    # fields - порядок и список полей, которые нужно отображать в форме редактирования
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    # readonly_fields - не редактируемые поля; указываем их, чтобы добавить в fields, иначе не будет работать!
    save_on_top = True  # добавляет панель удалить/сохранить наверх страницы редактирования

    # метод для отображения фото в админке, а не ссылки на него
    def get_html_photo(self, object):  # object будет ссылаться на текущую запись списка, те на объект модели Women
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50>')  # width=50 - размер отображения 50px
            # mark_safe - указывает не экранировать теги

    get_html_photo.short_description = 'Миниатюра'  # меняет название поля в таблице в админке


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах'
