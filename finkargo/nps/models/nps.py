from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from .user import User


# Create your models here.
class Entidad(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)


class Colaborador(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="user_colaborador", null=True)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="colaboradores")
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)


class Encuesta(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="encuesta_users", null=True)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    calificacion = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    fecha = models.DateTimeField(default=timezone.now)
    contactado = models.BooleanField(default=False)

    operative_sistem = models.CharField(max_length=255, null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)

 