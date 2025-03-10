from django.db import models

# Create your models here.

class actividades(models.Model):
    nombre=models.TextField()
    calorias=models.FloatField()
    eet=models.FloatField()


class foodlist(models.Model):
    Nombre = models.TextField()
    Energia = models.TextField()
    Cafeina = models.TextField()
    Alcohol = models.TextField()
    Agua = models.TextField()
    Proteina = models.TextField()
    Carbohidratos = models.TextField()
    Azucares = models.TextField()
    Fibra_total_dietetica = models.TextField()
    Grasa_total = models.TextField()
    Acidos_grasos_saturados = models.TextField()
    Acidos_grasos_monoinsaturados = models.TextField()
    Acidos_grasos_poliinsaturados = models.TextField()
    Colesterol = models.TextField()
    Vitamina_B6 = models.TextField()
    Vitamina_C = models.TextField()
    Vitamina_K = models.TextField()
    Calcio = models.TextField()
    Fosforo = models.TextField()
    Magnesio = models.TextField()
    Hierro = models.TextField()
    Zinc = models.TextField()
    Potasio = models.TextField()
    Sodio = models.TextField()
