from rest_framework import serializers
from django.db import models

from bus.models import Busstation, Buses, Tracking


class stationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busstation
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buses
        fields = '__all__'


class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = '__all__'