from django.urls import path

from women import views

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.WomenHome.as_view(), name='home'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),

    # path('addpage/', views.addpage, name='add_page'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),

    # path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),

    # path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
]
