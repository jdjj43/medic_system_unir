from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return redirect("login")


urlpatterns = [

    path(
        "",
        home,
        name="home"
    ),

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "usuarios/",
        include("usuarios.urls")
    ),

    path(
        "medicos/",
        include("medicos.urls")
    ),

    path(
        "pacientes/",
        include("pacientes.urls")
    ),

    path(
        "citas/",
        include("citas.urls")
    ),

    path(
        "historias/",
        include("historias.urls")
    ),

    path(
        "reportes/",
        include("reportes.urls")
    ),

    path(
        "auditoria/",
        include("auditoria.urls")
    ),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)