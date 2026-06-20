import re
from django import forms
from .models import SolicitudSimulacion


class SolicitudSimulacionForm(forms.ModelForm):
    class Meta:
        model = SolicitudSimulacion
        fields = [
            'nombre',
            'dni',
            'fecha_nacimiento',
            'email',
            'telefono',
            'ingreso_neto',
            'garante_nombre',
            'garante_fecha_nacimiento',
            'garante_tipo_trabajo',
            'garante_ingreso_neto',
            'garante_antiguedad',
            'modelo',
            'plan',
        ]

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+", nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")

        return nombre

    def clean_garante_nombre(self):
        nombre = self.cleaned_data['garante_nombre'].strip()

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+", nombre):
            raise forms.ValidationError("El nombre del garante solo puede contener letras y espacios.")

        return nombre

    def clean_dni(self):
        dni = self.cleaned_data['dni'].strip()

        if not re.fullmatch(r"\d{7,8}", dni):
            raise forms.ValidationError("El DNI debe tener 7 u 8 números.")

        return dni

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()

        if not re.fullmatch(r"[\d\s()+-]{8,20}", telefono):
            raise forms.ValidationError("El teléfono solo puede contener números, espacios, paréntesis, + o -.")

        return telefono

    def clean_ingreso_neto(self):
        ingreso = self.cleaned_data['ingreso_neto']

        if ingreso <= 0:
            raise forms.ValidationError("El ingreso neto debe ser mayor a 0.")

        return ingreso

    def clean_garante_ingreso_neto(self):
        ingreso = self.cleaned_data['garante_ingreso_neto']

        if ingreso <= 0:
            raise forms.ValidationError("El ingreso neto del garante debe ser mayor a 0.")

        return ingreso