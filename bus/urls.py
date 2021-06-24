from django.urls import path
from bus.views import (
    customer_get_stations,
    customer_get_buses, booking, cancel_booking, qr_api, occupied, tracking, camera, sensor, tracking_get
)

app_name = 'bus'
urlpatterns = [

    # url for user registration
    path('stations/', customer_get_stations, name='registration'),
    # url for user login
    path('busdetails/<int:id>/', customer_get_buses),
    path('booking/<int:id1>/<int:id2>/', booking, name="booking"),
    path('booking/cancel/<str:p>/', cancel_booking),
    path('qr/<int:id>/', qr_api),
    # path('oauth/login/', SocialLoginView.as_view())  # Fb login auth
    path('occupied/<int:id>/', occupied),
    path('tracking/', tracking),
    path('tracking-get/<int:id>/', tracking_get),
    path('camera/', camera),
    path('sensor/', sensor)
]
