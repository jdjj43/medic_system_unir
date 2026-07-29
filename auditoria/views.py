from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Auditoria
from usuarios.decorators import admin_required


@admin_required
def lista_auditoria(request):
    registros = Auditoria.objects.select_related("usuario").all().order_by("-fecha_hora")

    modulo_filtro = request.GET.get("modulo", "").strip()
    accion_filtro = request.GET.get("accion", "").strip()
    search_query = request.GET.get("q", "").strip()
    fecha_inicio = request.GET.get("fecha_inicio", "")
    fecha_fin = request.GET.get("fecha_fin", "")

    if modulo_filtro:
        registros = registros.filter(modulo__iexact=modulo_filtro)

    if accion_filtro:
        registros = registros.filter(accion__icontains=accion_filtro)

    if fecha_inicio:
        registros = registros.filter(fecha_hora__date__gte=fecha_inicio)

    if fecha_fin:
        registros = registros.filter(fecha_hora__date__lte=fecha_fin)

    if search_query:
        registros = registros.filter(
            Q(descripcion__icontains=search_query) |
            Q(usuario__username__icontains=search_query) |
            Q(usuario__first_name__icontains=search_query) |
            Q(usuario__last_name__icontains=search_query) |
            Q(direccion_ip__icontains=search_query)
        )

    modulos_disponibles = Auditoria.objects.values_list("modulo", flat=True).distinct().order_by("modulo")

    context = {
        "registros": registros[:200],
        "modulos_disponibles": modulos_disponibles,
        "modulo_filtro": modulo_filtro,
        "accion_filtro": accion_filtro,
        "search_query": search_query,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    }


    return render(
        request,
        "auditoria/lista_auditoria.html",
        context
    )
