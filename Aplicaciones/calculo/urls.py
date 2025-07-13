from django.urls import path 
from . import views 
from .views import vista_usuario_calculo
from .views import AdminDashboardView, UserDashboardView


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('dashboard/user/', UserDashboardView.as_view(), name='user-dashboard'),
    path('vista', vista_usuario_calculo, name='vista_usuario_calculo'),
    path('tipoGeneracion/', views.tipoGeneracion, name='tipoGeneracion'),
    path('central/<int:pk>/mapa/', views.central_mapa, name='central_mapa'),
    path('mapa/', views.mapa_general, name='mapa_general'),
    
    # Eleccion tipo
    path('centrales/<int:tipo_id>/', views.centrales_por_tipo, name='centrales_por_tipo'),

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

    # Fotovoltaica
    path('fotovoltaica/', views.FotovoltaicaListView.as_view(), name='fotovoltaica_list'),
    path('fotovoltaica/crear/', views.FotovoltaicaCreateView.as_view(), name='fotovoltaica_create'),
    path('fotovoltaica/<int:pk>/editar/', views.FotovoltaicaUpdateView.as_view(), name='fotovoltaica_update'),
    path('fotovoltaica/<int:pk>/eliminar/', views.FotovoltaicaDeleteView.as_view(), name='fotovoltaica_delete'),

    # Termica
    path('termica/', views.TermicaListView.as_view(), name='termica_list'),
    path('termica/crear/', views.TermicaCreateView.as_view(), name='termica_create'),
    path('termica/<int:pk>/editar/', views.TermicaUpdateView.as_view(), name='termica_update'),
    path('termica/<int:pk>/eliminar/', views.TermicaDeleteView.as_view(), name='termica_delete'),

    # Eolica
    path('eolica/', views.EolicaListView.as_view(), name='eolica_list'),
    path('eolica/crear/', views.EolicaCreateView.as_view(), name='eolica_create'),
    path('eolica/<int:pk>/editar/', views.EolicaUpdateView.as_view(), name='eolica_update'),
    path('eolica/<int:pk>/eliminar/', views.EolicaDeleteView.as_view(), name='eolica_delete'),

    # Hidraulica
    path('hidraulica/', views.HidraulicaListView.as_view(), name='hidraulica_list'),
    path('hidraulica/crear/', views.HidraulicaCreateView.as_view(), name='hidraulica_create'),
    path('hidraulica/<int:pk>/editar/', views.HidraulicaUpdateView.as_view(), name='hidraulica_update'),
    path('hidraulica/<int:pk>/eliminar/', views.HidraulicaDeleteView.as_view(), name='hidraulica_delete'),

    # InformacionCentral
    path('informacion/', views.InformacionCentralListView.as_view(), name='info_list'),
    path('informacion/nuevo/', views.InformacionCentralCreateView.as_view(), name='info_create'),
    path('informacion/editar/<int:pk>/', views.InformacionCentralUpdateView.as_view(), name='info_update'),
    path('informacion/eliminar/<int:pk>/', views.InformacionCentralDeleteView.as_view(), name='info_delete'),
    
    #path('calculo/detalle/<int:caso_id>/', views.detalle_calculo_lcoe, name='detalle_calculo_lcoe'),

    #path('tipo/<int:tipo_id>/', views.centrales_por_tipo, name='centrales_por_tipo'),

    #---- nuevo

    #path('calculo/', views.calculo_view, name='calculo_view'),
    path('caso/nuevo/', views.nuevo_caso_calculo, name='nuevo_caso_calculo'),

]
