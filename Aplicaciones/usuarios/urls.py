from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('redirect/', views.RedirectAfterLoginView.as_view(), name='redirect-after-login'),
    path('dashboard_admin/', views.vista_administrador, name='dashboard_admin'),
]
