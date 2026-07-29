from django.urls import path

from .views import (
    lista_pacientes,
    crear_paciente,
    editar_paciente,
    eliminar_paciente,
)


urlpatterns = [

    path(
        "lista/",
        lista_pacientes,
        name="lista_pacientes"
    ),

    path(
        "crear/",
        crear_paciente,
        name="crear_paciente"
    ),

    path(
        "<int:pk>/editar/",
        editar_paciente,
        name="editar_paciente"
    ),

    path(
        "<int:pk>/eliminar/",
        eliminar_paciente,
        name="eliminar_paciente"
    ),

]
