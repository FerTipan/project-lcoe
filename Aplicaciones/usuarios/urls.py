from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CustomLoginView, two_factor_login_view

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('redirect/', views.RedirectAfterLoginView.as_view(), name='redirect-after-login'),
    path('dashboard_admin/', views.vista_administrador, name='dashboard_admin'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('2fa/', two_factor_login_view, name='two_factor_login'),
]
