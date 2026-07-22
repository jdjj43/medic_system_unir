from django.db import models


class Paciente(models.Model):

    cedula = models.CharField(
        max_length=20,
        unique=True
    )

    nombres = models.CharField(
        max_length=100
    )

    apellidos = models.CharField(
        max_length=100
    )

    fecha_nacimiento = models.DateField(
        null=True,
        blank=True
    )

    sexo = models.CharField(
        max_length=20,
        choices=[
            ("M", "Masculino"),
            ("F", "Femenino"),
        ]
    )

    telefono = models.CharField(
        max_length=20
    )

    direccion = models.TextField(
        blank=True,
        null=True
    )

    correo = models.EmailField(
        blank=True,
        null=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.nombres} {self.apellidos}"