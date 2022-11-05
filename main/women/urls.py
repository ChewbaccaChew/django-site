from django.urls import path, re_path

from women import views

urlpatterns = [
    path('', views.index, name='home'),
    path('cats/<int:catid>/', views.categories),
    re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive),
]
