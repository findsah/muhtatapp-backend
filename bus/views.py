import os

from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
import json
from rest_framework.views import APIView

from users.models import SuperUser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from bus.serializers import BusSerializer, stationSerializer, TrackingSerializer
from bus.models import Buses, Busstation, Seats, Tracking, Camera, P_Sensor
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from PIL import Image
from pyzbar.pyzbar import decode


# Create your views here.
@api_view(['GET', ])
@csrf_exempt
@permission_classes([AllowAny])
def customer_get_stations(request):
    station = stationSerializer(
        Busstation.objects.all().order_by("-id"),
        many=True, context={"request": request}
    ).data
    content = []
    objs = Busstation.objects.all()
    for obj in objs:
        x = {'id': obj.id, 'name': obj.name,
             'coordinates': {'latitude': obj.location_lat, 'longitude': obj.location_long}}
        content.append(x)
    return Response(content)


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'], )
def customer_get_buses(request, id):
    remaining_seats = 50
    station = BusSerializer(
        Buses.objects.filter(station_id=id),
        many=True,
        context={"request": request}
    ).data
    buses_obj = Buses.objects.filter(station_id=id)
    x = 0
    for bus in buses_obj:
        seats = Seats.objects.filter(bus=bus).count()
        # print(seats)
        remaining_seats = 50 - seats
        station[x]['remaining_seats'] = remaining_seats
        x = x+1
    return JsonResponse({"station": station})


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'], )
def booking(request, id1, id2):
    user = SuperUser.objects.get(id=id1)
    bus_obj = Buses.objects.get(id=id2)
    id3 = 51
    for x in range(50):
        if Seats.objects.filter(bus=bus_obj, seat_number=x+1).count() != 0:
            x += 1
        else:
            id3 = x + 1
            break
    if 51 > id3 > 0:
        if user.cash > bus_obj.tprice:
            seat_obj = Seats.objects.create(passenger=user, seat_number=id3)
            seat_obj.bus.add(bus_obj)
            seat_obj.save()
            qrcode_img = qrcode.make(str(user.auth_token) + '_' + str(id3))
            canvas = Image.new('RGB', (390, 390), 'white')
            canvas.paste(qrcode_img)
            fname = f'bus_qr_code-{user.name}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            seat_obj.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
            seat_obj.save()
            user.cash -= bus_obj.tprice
            user.save()
            content = {'status': 'Seat Reserved', 'seat no.': id3,
                       'station': bus_obj.station.name, 'bus': bus_obj.name, 'qrcode': seat_obj.qr_code.url}
        else:
            content = {'status': 'Not Enough Cash'}
    else:
        content = {'status': 'No Seats Available'}

    return Response(content, status=status.HTTP_200_OK)


@api_view(['POST'], )
@permission_classes([AllowAny])
def qr_api(request, id):
    qr = Seats.objects.filter(id=id)
    qs2 = serializers.serialize("json", qr)
    return Response(json.loads(qs2))


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'], )
def cancel_booking(request, p):
    # img = request.FILES.get('image')
    # d = decode(Image.open(img))
    # p = d[0].data.decode('ascii')
    length = len(p)
    y = []
    z = 1
    for x in p:
        if x == '_':
            y.append(z)
        z += 1
    seat_number = p[y[0]:]
    p = p[:y[0]-1]
    if SuperUser.objects.filter(auth_token=p).count() != 0:
        user = SuperUser.objects.get(auth_token=p)

        if Seats.objects.filter(passenger=user, seat_number=seat_number).count() != 0:
            seat_obj = Seats.objects.get(passenger=user, seat_number=seat_number)
            seat_obj.delete()
            content = {'status': 'Qr Deleted'}
        else:
            content = {'status': 'No such Qr'}
    else:
        content = {'status': 'No such User'}
    return Response(content, status=status.HTTP_200_OK)


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'], )
def occupied(request, id):
    bus = Buses.objects.get(id=id)
    seats = Seats.objects.filter(bus=bus)
    occupied = []
    not_occupied = []
    y = []
    for x in range(bus.capacity):
        not_occupied.append(x + 1)
    for seat in seats:
        occupied.append(seat.seat_number)
        num = seat.seat_number
        not_occupied.remove(num)

    # print(not_occupied)
    return Response({'Occupied_Seats': occupied, 'Not_Occupied_Seats': not_occupied}, status=status.HTTP_200_OK)


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'], )
def tracking(request):
    long = request.data.get('longitude')
    lat = request.data.get('latitude')
    time = request.data.get('timestamp')
    bus_id = request.data.get('bus_id')

    num = Tracking.objects.filter(bus_id=bus_id).count()

    if num != 0:
        track_obj = Tracking.objects.get(bus_id=bus_id)
        track_obj.long = long
        track_obj.lat = lat
        track_obj.timestamp = time
        track_obj.save()
    else:
        Tracking.objects.create(bus_id=bus_id, long=long, lat=lat, timestamp=time)

    return Response({'longitude': long, 'latitude': lat, 'timestamp': time, 'bus': bus_id})


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'], )
def camera(request):
    bus_id = request.data.get('bus_id')
    time = request.data.get('time')
    file = request.data.get('file')
    Camera.objects.create(bus_id=bus_id, time=time, filename=file)
    return Response(status=status.HTTP_200_OK)


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'], )
def sensor(request):
    bus_id = request.data.get('bus_id')
    pass_count = request.data.get('pass_count')
    date_time = request.data.get('date_time')
    P_Sensor.objects.create(bus_id=bus_id, pass_count=pass_count, date_time=date_time)
    return Response(status=status.HTTP_200_OK)


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['GET'], )
def tracking_get(request, id):
    if Tracking.objects.filter(bus_id=id).count() != 0:
        t = Tracking.objects.get(bus_id=id)
        s = TrackingSerializer(t)

        return Response(s.data, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'No such Bus'}, status=status.HTTP_404_NOT_FOUND)