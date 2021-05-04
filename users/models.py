from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.

class CustomUser(BaseUserManager):
    """

	Custom user model manager where email is the Unique identifier
	for authentication instead of username.

	"""

    def _create_user(self, email, password, is_active, is_staff, is_superuser, **extra_fields):
        """
		Create and save a User with the given email and password.
		"""
        if not email:
            raise ValueError(_('Email must be provided.'))

        if not password:
            raise ValueError(_('Password must be provided.'))

        email = self.normalize_email(email)  # normalize_email is used to validate the given email.
        user = self.model(email=email, is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):

        return self._create_user(email, password, is_active=True, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, email, password, is_active=True, is_staff=True, is_superuser=True, **extra_fields):
        '''
		It will create a superuser with the given email and password
		'''
        user = self._create_user(email, password, is_staff=True, is_active=True, is_superuser=True, **extra_fields)
        user.save(using=self._db)
        return user


class SuperUser(AbstractBaseUser, PermissionsMixin):
    """docstring for ClassName"""
    username = None
    email = models.EmailField(_('Email Address'), unique=True)
    name = models.CharField(_('first Name'), blank=True, max_length=200)
    phone = models.CharField(_('phone'), blank=True, max_length=200)
    # qr_code = models.ImageField(upload_to='', blank=True, null=True)
    cash = models.IntegerField(default=100, null=True, blank=True)
    # b_qr_code = models.ImageField(upload_to='buses_qr', blank=True, null=True)
    captain = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone',]

    objects = CustomUser()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.name)

    # def save(self, *args, **kwargs):
    #     qrcode_img = qrcode.make(self.name)
    #     canvas = Image.new('RGB', (290, 290), 'white')
    #     draw = ImageDraw.Draw(canvas)
    #     canvas.paste(qrcode_img)
    #     fname = f'qr_code-{self.name}.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer,'PNG')
    #     self.qr_code.save(fname, File(buffer), save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)
    # def get_full_name(self):
    #     """
    #     Return the first_name plus the last_name, with a space in between.
    #     """
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def token_creation(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)