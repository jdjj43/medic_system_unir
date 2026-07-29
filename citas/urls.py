from django.urls import path

from .views import (
    lista_citas,
    crear_cita,
    editar_cita,
    eliminar_cita,
)


urlpatterns = [

    path(
        "lista/",
        lista_citas,
        name="lista_citas"
    ),

    path(
        "crear/",
        crear_cita,
        name="crear_cita"
    ),

    path(
        "<int:pk>/editar/",
        editar_cita,
        name="editar_cita"
    ),

    path(
        "<int:pk>/eliminar/",
        eliminar_cita,
        name="eliminar_cita"
    ),

]
