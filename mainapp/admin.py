from django.contrib import admin
from usuarios.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'altura', 'peso', 'genero','edad'
        )

admin.site.register(CustomUser, CustomUserAdmin)
