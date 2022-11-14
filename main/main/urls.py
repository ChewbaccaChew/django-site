"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from women import views
from main import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('women.urls')),
]

# в режиме отладки к маршрутам добавляем доп пути: для django-debug-toolbar и для статических файлов
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# обработка исключений при запросах к серверу
# работают только при DEBUG = False в settings.py
handler404 = views.page_not_found
# handler500 - ошибка сервера
# handler403 - доступ запрещен
# handler400 - невозможно обработать запрос
