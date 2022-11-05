from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse('Страница приложения Women')


def categories(request, catid):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)

    return HttpResponse(f'Статьи по категориям<p>{catid}</p>')


def archive(request, year):
    if int(year) > 2020:
        # raise Http404()
        # return redirect('home')  # перенаправляет на главную, код 302 (временный url)
        return redirect('home', permanent=True)  # код 301 (постоянный url)

    return HttpResponse(f'Архив по годам<p>{year}</p>')


def page_not_found(request, exception):
    # функция для отображения ненайденных страниц
    return HttpResponseNotFound('Страница не найдена')
