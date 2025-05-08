from django.urls import path 
<<<<<<< HEAD
from . import views 

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tipoGeneracion/', views.tipoGeneracion, name='tipoGeneracion'),

    # Eleccion tipo
    path('centrales/<int:tipo_id>/', views.centrales_por_tipo, name='centrales_por_tipo'),

    path('hidraulica/', views.hidraulica, name='hidraulica'),
    path('termica/', views.termica, name='termica'),
    path('solar/', views.solar, name='solar'),  
    path('eolica/', views.eolica, name='eolica'),

    path('login/', views.login, name='login'),

    # TipoElectrica
    path('tipoelectrica/', views.TipoElectricaListView.as_view(), name='tipoelectrica_list'),
    path('tipoelectrica/nuevo/', views.TipoElectricaCreateView.as_view(), name='tipoelectrica_create'),
    path('tipoelectrica/editar/<int:pk>/', views.TipoElectricaUpdateView.as_view(), name='tipoelectrica_update'),
    path('tipoelectrica/eliminar/<int:pk>/', views.TipoElectricaDeleteView.as_view(), name='tipoelectrica_delete'),

    # Central
    path('central/', views.CentralListView.as_view(), name='central_list'),
    path('central/nuevo/', views.CentralCreateView.as_view(), name='central_create'),
    path('central/editar/<int:pk>/', views.CentralUpdateView.as_view(), name='central_update'),
    path('central/eliminar/<int:pk>/', views.CentralDeleteView.as_view(), name='central_delete'),

    # InformacionCentral
    path('informacion/', views.InformacionCentralListView.as_view(), name='info_list'),
    path('informacion/nuevo/', views.InformacionCentralCreateView.as_view(), name='info_create'),
    path('informacion/editar/<int:pk>/', views.InformacionCentralUpdateView.as_view(), name='info_update'),
    path('informacion/eliminar/<int:pk>/', views.InformacionCentralDeleteView.as_view(), name='info_delete'),
    
    path('ajax/info-central/<int:central_id>/', views.obtener_info_central, name='ajax_info_central'),

]
=======
from . import views
urlpatterns=[
    path('', views.inicio)
]
>>>>>>> a3dff5b01aab34fea0a7f46772be1cbf69f495e5
