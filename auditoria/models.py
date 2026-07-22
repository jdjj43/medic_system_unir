from django.db import models
from usuarios.models import Usuario


class RegistroActividad(models.Model):

    TIPOS_ACCION = [

        ("LOGIN", "Inicio de sesión"),

        ("LOGOUT", "Cierre de sesión"),

        ("CREAR", "Crear"),

        ("ACTUALIZAR", "Actualizar"),

        ("ELIMINAR", "Eliminar"),

        ("CONSULTAR", "Consultar"),

    ]


    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name="actividades"
    )


    accion = models.CharField(
        max_length=20,
        choices=TIPOS_ACCION
    )


    modelo = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    objeto_id = models.IntegerField(
        blank=True,
        null=True
    )


    descripcion = models.TextField(
        blank=True,
        null=True
    )


    fecha = models.DateTimeField(
        auto_now_add=True
    )


    direccion_ip = models.GenericIPAddressField(
        blank=True,
        null=True
    )


    class Meta:

        ordering = [
            "-fecha"
        ]


    def __str__(self):

        return f"{self.usuario} - {self.accion}"