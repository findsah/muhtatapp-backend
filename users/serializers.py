from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from users.models import SuperUser


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    name = serializers.CharField(max_length=200, required=False)
    phone = serializers.IntegerField(required=False)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate_email(self, value):
        """
        Check that the valid email with @gmail.com is provided by the user or not in the given email.
        """
        data = self.get_initial()
        email = data.get('email')
        # password = value
        user_email = SuperUser.objects.filter(email=email)

        if user_email:
            raise ValidationError("User with this email already exists.")
            return False
        return value

    def save(self):
        account = SuperUser(

            email=self.validated_data['email'],
            # name       = self.validated_data['name'],
            name=self.validated_data['name'],
            phone=self.validated_data['phone'],
        )

        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise ValidationError(_("Both passwords doesn't match"))
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )


def validate(self, attrs):
    email = attrs.get('email', None)
    password = attrs.get('password')

    if email and password:
        user = authenticate(request=self.context.get('request'),
                            email=email, password=password)
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
    else:
        msg = _('Must include "email" and "password".')
        raise serializers.ValidationError(msg, code='authorization')

    attrs['user'] = user
    return attrs

