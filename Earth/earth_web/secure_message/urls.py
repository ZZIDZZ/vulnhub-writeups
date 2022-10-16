from django.urls import path
from django.contrib.auth import views as admin_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin, name='admin'),
    path('admin/login', admin_views.LoginView.as_view(), name='login'),
    path('admin/logout', admin_views.LogoutView.as_view(), name='logout'),
]
