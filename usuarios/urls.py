from django.urls import path
from .views import vista_registro, cerrar_sesion,login_view

urlpatterns = [
    path('login/', login_view, name="login"),
    path('registrar/', vista_registro.as_view(), name="registrar"),
    path('cerrar_sesion/', cerrar_sesion, name="cerrar_sesion")
]
