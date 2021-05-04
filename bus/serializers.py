from rest_framework import serializers
from django.db import models

from bus.models import Busstation, Buses


class stationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busstation
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buses
        fields = '__all__'
