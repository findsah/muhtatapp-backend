from django.contrib import admin
from bus.models import Busstation, Buses, Seats


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
