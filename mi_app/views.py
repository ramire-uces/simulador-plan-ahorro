from datetime import date
from decimal import Decimal

import requests

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from .forms import SolicitudSimulacionForm
from .models import SolicitudSimulacion
from .serializers import SolicitudSimulacionSerializer


VEHICULOS = {
    'Auron City': Decimal('8500000'),
    'Velkar Nova': Decimal('10200000'),
    'Oryex Prime': Decimal('12800000'),
    'Zenthor': Decimal('15500000'),
}

PLANES = {
    'Plan 70/30': Decimal('0.30'),
    'Plan 60/40': Decimal('0.40'),
}


def pagina_inicio(request):
    return render(request, 'mi_app/index.html')


def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


def obtener_dolar_oficial():
    try:
        respuesta = requests.get('https://dolarapi.com/v1/dolares/oficial', timeout=8)
        respuesta.raise_for_status()
        datos = respuesta.json()
        return Decimal(str(datos.get('venta')))
    except Exception:
        return None


def calcular_plan(modelo, plan):
    precio = VEHICULOS[modelo]
    porcentaje_adjudicacion = PLANES[plan]

    importe_adjudicacion = precio * porcentaje_adjudicacion
    importe_retiro = Decimal('500000')
    cantidad_cuotas = 84
    tasa_interes = Decimal('14.50')

    monto_financiado = precio - importe_adjudicacion
    monto_total = (monto_financiado + importe_retiro) * (Decimal('1') + tasa_interes / Decimal('100'))
    cuota_mensual = monto_total / cantidad_cuotas

    return {
        'precio_vehiculo': precio,
        'importe_adjudicacion': importe_adjudicacion,
        'importe_retiro': importe_retiro,
        'cantidad_cuotas': cantidad_cuotas,
        'tasa_interes': tasa_interes,
        'cuota_mensual': cuota_mensual.quantize(Decimal('0.01')),
    }


def enviar_correo_confirmacion(solicitud):
    asunto = 'Confirmación de simulación de plan de ahorro'

    mensaje = f"""
Hola {solicitud.nombre}.

Tu solicitud fue cargada correctamente.

Informe final:

Modelo seleccionado: {solicitud.modelo}
Plan elegido: {solicitud.plan}
Precio del vehículo: ${solicitud.precio_vehiculo}
Cantidad de cuotas: {solicitud.cantidad_cuotas}
Importe para adjudicación: ${solicitud.importe_adjudicacion}
Importe para retiro: ${solicitud.importe_retiro}
Tasa de interés: {solicitud.tasa_interes}%
Cuota mensual estimada: ${solicitud.cuota_mensual}

Datos del titular:
DNI: {solicitud.dni}
Teléfono: {solicitud.telefono}
Ingreso neto mensual: ${solicitud.ingreso_neto}

Datos del garante:
Nombre: {solicitud.garante_nombre}
Tipo de trabajo: {solicitud.garante_tipo_trabajo}
Ingreso neto mensual: ${solicitud.garante_ingreso_neto}
Antigüedad laboral: {solicitud.garante_antiguedad} año/s
"""

    try:
        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [solicitud.email],
            fail_silently=False,
        )
        return True
    except Exception as error:
        print("Error enviando correo:", error)
        return False


@require_GET
def cotizacion_dolar(request):
    dolar = obtener_dolar_oficial()

    if dolar is None:
        return JsonResponse({
            'ok': False,
            'mensaje': 'No se pudo obtener la cotización del dólar oficial.',
        }, status=503)

    return JsonResponse({
        'ok': True,
        'dolar_oficial': float(dolar),
    })


@require_POST
def crear_solicitud(request):
    form = SolicitudSimulacionForm(request.POST)

    if not form.is_valid():
        errores = form.errors.get_json_data()
        primer_error = "Revisá los datos ingresados."

        for campo, lista_errores in errores.items():
            if lista_errores:
                primer_error = lista_errores[0]["message"]
                break

        return JsonResponse({
            'ok': False,
            'mensaje': primer_error,
            'errores': errores,
        }, status=400)

    datos = form.cleaned_data

    edad_titular = calcular_edad(datos['fecha_nacimiento'])
    edad_garante = calcular_edad(datos['garante_fecha_nacimiento'])

    if edad_titular < 18:
        return JsonResponse({
            'ok': False,
            'mensaje': 'El titular debe tener como mínimo 18 años.',
        }, status=400)

    if edad_titular > 75:
        return JsonResponse({
            'ok': False,
            'mensaje': 'El titular no puede superar los 75 años al finalizar el plan.',
        }, status=400)

    if edad_garante < 18:
        return JsonResponse({
            'ok': False,
            'mensaje': 'El garante debe tener como mínimo 18 años.',
        }, status=400)

    if datos['garante_tipo_trabajo'] == 'Relación de dependencia' and datos['garante_antiguedad'] < 1:
        return JsonResponse({
            'ok': False,
            'mensaje': 'El garante en relación de dependencia debe tener al menos 1 año de antigüedad.',
        }, status=400)

    if datos['garante_tipo_trabajo'] == 'Independiente' and datos['garante_antiguedad'] < 2:
        return JsonResponse({
            'ok': False,
            'mensaje': 'El garante independiente debe tener al menos 2 años de antigüedad.',
        }, status=400)

    calculo = calcular_plan(datos['modelo'], datos['plan'])

    if datos['garante_ingreso_neto'] < calculo['cuota_mensual'] * Decimal('4'):
        return JsonResponse({
            'ok': False,
            'mensaje': 'El ingreso del garante debe ser mayor a 4 veces el valor de la cuota.',
        }, status=400)

    dolar = obtener_dolar_oficial()

    solicitud = form.save(commit=False)
    solicitud.precio_vehiculo = calculo['precio_vehiculo']
    solicitud.importe_adjudicacion = calculo['importe_adjudicacion']
    solicitud.importe_retiro = calculo['importe_retiro']
    solicitud.cantidad_cuotas = calculo['cantidad_cuotas']
    solicitud.tasa_interes = calculo['tasa_interes']
    solicitud.cuota_mensual = calculo['cuota_mensual']
    solicitud.dolar_oficial = dolar
    solicitud.save()

    correo_enviado = enviar_correo_confirmacion(solicitud)

    return JsonResponse({
        'ok': True,
        'mensaje': 'La solicitud fue cargada correctamente.' if correo_enviado else 'La solicitud fue cargada correctamente, pero no se pudo enviar el correo de confirmación.',
        'informe': {
            'modelo': solicitud.modelo,
            'plan': solicitud.plan,
            'precio_vehiculo': float(solicitud.precio_vehiculo),
            'importe_adjudicacion': float(solicitud.importe_adjudicacion),
            'importe_retiro': float(solicitud.importe_retiro),
            'cantidad_cuotas': solicitud.cantidad_cuotas,
            'tasa_interes': float(solicitud.tasa_interes),
            'cuota_mensual': float(solicitud.cuota_mensual),
            'dolar_oficial': float(solicitud.dolar_oficial) if solicitud.dolar_oficial else None,
        }
    })


@staff_member_required
def panel_solicitudes(request):
    solicitudes = SolicitudSimulacion.objects.all().order_by('-creada_en')
    return render(request, 'mi_app/panel_solicitudes.html', {
        'solicitudes': solicitudes,
    })


@api_view(['GET'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def api_solicitudes(request):
    solicitudes = SolicitudSimulacion.objects.all().order_by('-creada_en')
    serializer = SolicitudSimulacionSerializer(solicitudes, many=True)
    return Response(serializer.data)