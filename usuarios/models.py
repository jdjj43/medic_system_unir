from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Rol(models.TextChoices):
    ADMIN = "ADMIN", "Administrador"
    MEDICO = "MEDICO", "Médico"
    RECEPCION = "RECEPCION", "Recepcionista"

class Usuario(AbstractUser):
    rol = models.CharField(
        max_length=15,
        choices=Rol.choices,
        default=Rol.RECEPCION,
        verbose_name="Rol"
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"