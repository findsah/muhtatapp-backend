from django.db import models
from users.models import SuperUser
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class Busstation(models.Model):
    name = models.CharField(max_length=500)
    location_long = models.CharField(max_length=1000, null=True, default=45.4215)
    location_lat = models.CharField(max_length=1000, null=True, default=45.4215)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bus Station"
        verbose_name_plural = "Bus Stations"


class Buses(models.Model):
    station = models.ForeignKey(Busstation, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500)
    tprice = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    start_time = models.CharField(max_length=1000, null=True)
    end_time = models.CharField(max_length=1000, null=True)
    destination = models.CharField(max_length=500, default='Ferozepur')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"


class Seats(models.Model):
    seat_number = models.IntegerField(_("Ticket Number"))
    passenger = models.ForeignKey(SuperUser, on_delete=models.CASCADE, related_name='seats')
    bus = models.ManyToManyField(Buses, related_name='seat')
    qr_code = models.ImageField(upload_to='buses_qr')

    def delete(self, *args, **kwargs):
        self.qr_code.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"


class Tracking(models.Model):
    long = models.CharField(max_length=300)
    lat = models.CharField(max_length=300)
    timestamp = models.CharField(max_length=300)
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE, default=1)


class Camera(models.Model):
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE)
    time = models.CharField(max_length=300)
    filename = models.CharField(max_length=500)


class P_Sensor(models.Model):
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE)
    pass_count = models.IntegerField()
    date_time = models.CharField(max_length=400)

