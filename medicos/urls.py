from django.urls import path

from .views import (
    lista_especialidades,
    crear_especialidad,
    editar_especialidad,
    eliminar_especialidad,
    lista_medicos,
    crear_medico,
    editar_medico,
    eliminar_medico,
)


urlpatterns = [

    path(
        "especialidades/",
        lista_especialidades,
        name="lista_especialidades"
    ),

    path(
        "especialidades/crear/",
        crear_especialidad,
        name="crear_especialidad"
    ),

    path(
        "especialidades/<int:pk>/editar/",
        editar_especialidad,
        name="editar_especialidad"
    ),

    path(
        "especialidades/<int:pk>/eliminar/",
        eliminar_especialidad,
        name="eliminar_especialidad"
    ),

    path(
        "lista/",

        lista_medicos,
        name="lista_medicos"
    ),

    path(
        "crear/",
        crear_medico,
        name="crear_medico"
    ),

    path(
        "<int:pk>/editar/",
        editar_medico,
        name="editar_medico"
    ),

    path(
        "<int:pk>/eliminar/",
        eliminar_medico,
        name="eliminar_medico"
    ),

]
