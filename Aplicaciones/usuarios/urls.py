from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.redireccion_por_rol, name='inicio_redireccion'),
    path('admin-dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('logout/', views.custom_logout, name='logout'),
]
