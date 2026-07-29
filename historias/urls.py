from django.urls import path

from .views import (
    lista_historias,
    crear_historia,
    editar_historia,
    eliminar_historia,
    subir_archivo,
    eliminar_archivo,
)


urlpatterns = [

    path(
        "lista/",
        lista_historias,
        name="lista_historias"
    ),

    path(
        "crear/",
        crear_historia,
        name="crear_historia"
    ),

    path(
        "<int:pk>/editar/",
        editar_historia,
        name="editar_historia"
    ),

    path(
        "<int:pk>/eliminar/",
        eliminar_historia,
        name="eliminar_historia"
    ),

    path(
        "<int:pk>/subir-archivo/",
        subir_archivo,
        name="subir_archivo"
    ),

    path(
        "archivo/<int:pk>/eliminar/",
        eliminar_archivo,
        name="eliminar_archivo"
    ),

]
