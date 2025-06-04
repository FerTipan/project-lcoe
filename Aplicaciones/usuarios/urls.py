from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CustomLoginView, RedirectAfterLoginView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),

    #path('login/', views.login_view, name='login'),
    #path('', views.redireccion_por_rol, name='inicio_redireccion'),
    path('logout/', views.custom_logout, name='logout'),
    path('redirect/', RedirectAfterLoginView.as_view(), name='redirect-after-login'),

]
