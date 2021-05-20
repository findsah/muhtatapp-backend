from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode
from rest_framework.views import APIView

from users.models import SuperUser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
import pyqrcode
from PIL import Image
from .models import SuperUser
import json
from django.core import serializers



# Create your views here.

@api_view(['GET'])
def home_view(request):
    return Response(
        {

            'url for get-station': ' if you are offline => http://127.0.0.1:8000/buses/stations/ if you are online =>'
                                    'https://muhtat-app.herokuapp.com/buses/stations/',
            'url for get buses': ' if you are offline => http://127.0.0.1:8000/buses/busdetails/id/ if you are online => '
                                     'https://muhtat-app.herokuapp.com/buses/busdetails/id/ ',
            'url for registration': ' if you are offline => http://127.0.0.1:8000/registration/api/registration/ if '
                                    'you are online => https://eign-backend.herokuapp.com/user/registration/'
                                    '/ ',
            'url for login': ' if you are offline => http://127.0.0.1:8000/user/login/ if you are online => https://'
                             'eign-backend.herokuapp.com/user/login/ ',

        }
    )

@api_view(['POST'], )
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()

        data['response'] = "User created successfully! wohooo"
        data['email'] = account.email
        data['name'] = account.name
        data['phone'] = account.phone
        token = Token.objects.get(user=account).key
        data['token'] = token

        current_site = get_current_site(request)
        subject = 'Activate Your MySite Account'
        site_url = 'http://%s/activate/%s/%s' % (
            current_site.domain, urlsafe_base64_encode(force_bytes(SuperUser.pk)),
            data['token'])
        message = "Please Confirm Your Email To Complete Registration: " + site_url
        send_mail('From Basaier', message, "hamza@gmail.com", [account.email])
        messages.success(request, ('Please Confirm Your Email To Complete Registration.'))

        # qr = pyqrcode.create(token)
        # qr.png(account.email + '.png', scale=8)
        # img = Image.open(account.email + '.png')
        # print(img)
        # account.qrcode = img
        account.save()
        # qr.png(account.email + '.png', scale=8)
    else:
        data = serializer.errors
    return Response(data)


@permission_classes([AllowAny])
class CustomAuthToken(ObtainAuthToken):
    serializer_class1 = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class1(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        if SuperUser.objects.filter(email=email).count() != 0:

            user1 = SuperUser.objects.get(email=email)
            user = authenticate(email=email, password=password)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                # 'name': user.name,
                # 'first_name': user.first_name,
                # 'last_name': user.last_name,
                'name': user.name,
                'driver': user.driver,
                'cash': user.cash,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'No such User'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            token = request.POST.get('token')
            user = SuperUser.objects.get(auth_token=token)
            print(user)
            # SuperUser.objects.filter(id=userid).update(auth_token='')
            user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        return response



@api_view(['POST'], )
@permission_classes([AllowAny])
def qr_api(request, id):
    user = SuperUser.objects.filter(id=id)
    qs2 = serializers.serialize("json", user)

    return Response(json.loads(qs2))
