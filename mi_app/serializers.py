from rest_framework import serializers
from .models import SolicitudSimulacion


class SolicitudSimulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudSimulacion
        fields = '__all__'