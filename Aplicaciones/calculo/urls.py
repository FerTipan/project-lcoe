from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tipoGeneracion/', views.tipoGeneracion, name='tipoGeneracion'),
    path('hidraulica/', views.hidraulica, name='hidraulica'),
    path('termica/', views.termica, name='termica'),
    path('solar/', views.solar, name='solar'),  
    path('eolica/', views.eolica, name='eolica'),
]