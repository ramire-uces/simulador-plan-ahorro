from django.db import models


class SolicitudSimulacion(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    email = models.EmailField()
    telefono = models.CharField(max_length=30)
    ingreso_neto = models.DecimalField(max_digits=12, decimal_places=2)

    garante_nombre = models.CharField(max_length=100)
    garante_fecha_nacimiento = models.DateField()
    garante_tipo_trabajo = models.CharField(max_length=40)
    garante_ingreso_neto = models.DecimalField(max_digits=12, decimal_places=2)
    garante_antiguedad = models.PositiveIntegerField()

    modelo = models.CharField(max_length=50)
    plan = models.CharField(max_length=20)

    precio_vehiculo = models.DecimalField(max_digits=12, decimal_places=2)
    importe_adjudicacion = models.DecimalField(max_digits=12, decimal_places=2)
    importe_retiro = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad_cuotas = models.PositiveIntegerField(default=84)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    cuota_mensual = models.DecimalField(max_digits=12, decimal_places=2)

    dolar_oficial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} - {self.modelo} - {self.plan}'
