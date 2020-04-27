from django.conf import settings
from django.db import models
from django.utils import timezone


class Examen(models.Model):
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tema = models.CharField(max_length=200)
    fecha = models.DateTimeField(default=timezone.now)
    preguntas = models.TextField(blank=True, max_length=10000, default="")
    respuestas = models.TextField(blank=True, max_length=10000, default="")
    opcional = models.TextField(blank=True, max_length=10000, default="")
    crear_pregunta = models.TextField(blank=True, max_length=10000, default="")
