from django.contrib import admin
from .models import SolicitudSimulacion


@admin.register(SolicitudSimulacion)
class SolicitudSimulacionAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'dni',
        'email',
        'modelo',
        'plan',
        'cuota_mensual',
        'creada_en',
    )

    search_fields = (
        'nombre',
        'dni',
        'email',
        'modelo',
    )

    list_filter = (
        'modelo',
        'plan',
        'creada_en',
    )

    readonly_fields = (
        'precio_vehiculo',
        'importe_adjudicacion',
        'importe_retiro',
        'cantidad_cuotas',
        'tasa_interes',
        'cuota_mensual',
        'dolar_oficial',
        'creada_en',
    )