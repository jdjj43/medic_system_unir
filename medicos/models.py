from django.db import models
from usuarios.models import Usuario


class Especialidad(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )


    def __str__(self):
        return self.nombre



class Medico(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_medico"
    )

    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name="medicos"
    )

    numero_licencia = models.CharField(
        max_length=50,
        unique=True
    )

    consultorio = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


    def __str__(self):
        return f"Dr. {self.usuario.first_name} {self.usuario.last_name}"