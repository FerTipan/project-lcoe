from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tipo/', views.tipoGeneracion, name='tipoGeneracion'),
    path('eolica/', views.eolica, name='eolica'),
    path('solar/', views.solar, name='solar'),
    path('hidraulica/', views.hidraulica, name='hidraulica'),
    path('termica/', views.termica, name='termica'),
]