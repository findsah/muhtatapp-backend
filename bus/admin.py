from django.contrib import admin
from bus.models import Busstation, Buses, Seats, Tracking, Camera, P_Sensor


@admin.register(Busstation)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

    class Meta:
        model = Busstation


@admin.register(Buses)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'capacity']

    class Meta:
        model = Buses


@admin.register(Seats)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['seat_number', 'passenger']

    class Meta:
        model = Seats


@admin.register(Tracking)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'long', 'lat', 'timestamp', 'bus']

    class Meta:
        model = Tracking


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus', 'time', 'filename']

    class Meta:
        model = Camera


@admin.register(P_Sensor)
class P_SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus', 'pass_count', 'date_time']

    class Meta:
        model = P_Sensor