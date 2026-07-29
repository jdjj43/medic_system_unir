from django.urls import path

from .views import (
    login_view,
    logout_view,
    dashboard,
    lista_usuarios,
    crear_usuario,
    editar_usuario,
    eliminar_usuario,
)


urlpatterns = [

    path(
        "login/",
        login_view,
        name="login"
    ),

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),

    path(
        "lista/",
        lista_usuarios,
        name="lista_usuarios"
    ),

    path(
        "crear/",
        crear_usuario,
        name="crear_usuario"
    ),

    path(
        "<int:pk>/editar/",
        editar_usuario,
        name="editar_usuario"
    ),

    path(
        "<int:pk>/eliminar/",
        eliminar_usuario,
        name="eliminar_usuario"
    ),

]