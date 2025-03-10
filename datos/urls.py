from django.urls import path
from .views import vista_actividades, vista_nutricion

urlpatterns = [
    path('nutricion/', vista_nutricion, name="nutricion"),
    path('nutricion/<int:id>/', vista_nutricion, name="nutricion_with_id"),
    path('actividades/', vista_actividades, name="actividades"),
]
