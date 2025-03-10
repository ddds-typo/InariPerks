from django.urls import path
from .views import contacto

urlpatterns = [
    path('contacto/', contacto, name="contacto"),
]
