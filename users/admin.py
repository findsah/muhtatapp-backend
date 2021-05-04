from django.contrib import admin
from users.models import SuperUser

# Register your models here.

@admin.register(SuperUser)
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
