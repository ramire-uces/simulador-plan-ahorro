from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='index'),
    path('solicitudes/crear/', views.crear_solicitud, name='crear_solicitud'),
    path('cotizacion-dolar/', views.cotizacion_dolar, name='cotizacion_dolar'),
    path('panel/solicitudes/', views.panel_solicitudes, name='panel_solicitudes'),
    path('api/solicitudes/', views.api_solicitudes, name='api_solicitudes'),
]
