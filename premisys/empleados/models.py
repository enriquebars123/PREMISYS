from django.db import models
from django.utils import timezone

# Create your models here.

class Empleado(models.Model):
    aduana = models.IntegerField(
        null=False, 
        blank=False
    )
    turno = models.IntegerField(
        null=False, 
        blank=False
    )
    nomina = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    nombre = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    area_origen = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    area_destino = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    motivo = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    epp = models.BooleanField(default=False,)
    lentes = models.BooleanField(default=False,)
    caretas = models.BooleanField(default=False,)
    cubrebocas = models.BooleanField(default=False,)
    nomina_aduana = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True,)

    class Meta:
        db_table = 'meraki_registro_empleados'

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre


class EmpleadoExcel(models.Model):
    nomina = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    nombre = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    planta = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    mac = models.CharField(
        max_length=255, 
        null=False, 
        blank=False
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True,)

    class Meta:
        db_table = 'meraki_registro_empleados_excel'

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre
