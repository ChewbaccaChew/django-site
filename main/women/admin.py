from django.contrib import admin

from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')  # поля отображаемые в админке
    list_display_links = ('id', 'title')  # поля-ссылки
    search_fields = ('title', 'content')  # поля по которым будет осуществляться поиск
    list_filter = ('is_published', 'time_create')  # поля по которым возможна фильтрация
    list_editable = ('is_published',)  # поля редактируемые прямо в админке


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
