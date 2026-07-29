import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from citas.models import Cita
from pacientes.models import Paciente
from medicos.models import Medico, Especialidad
from historias.models import HistorialMedico


@login_required
def panel_reportes(request):
    fecha_inicio = request.GET.get("fecha_inicio", "")
    fecha_fin = request.GET.get("fecha_fin", "")
    medico_id = request.GET.get("medico", "")
    especialidad_id = request.GET.get("especialidad", "")
    estado = request.GET.get("estado", "")

    citas_qs = Cita.objects.select_related("paciente", "medico", "medico__usuario", "medico__especialidad").all()
    historias_qs = HistorialMedico.objects.select_related("paciente", "medico", "medico__usuario").all()

    if fecha_inicio:
        citas_qs = citas_qs.filter(fecha__gte=fecha_inicio)
        historias_qs = historias_qs.filter(fecha__date__gte=fecha_inicio)

    if fecha_fin:
        citas_qs = citas_qs.filter(fecha__lte=fecha_fin)
        historias_qs = historias_qs.filter(fecha__date__lte=fecha_fin)

    if medico_id:
        citas_qs = citas_qs.filter(medico_id=medico_id)
        historias_qs = historias_qs.filter(medico_id=medico_id)

    if especialidad_id:
        citas_qs = citas_qs.filter(medico__especialidad_id=especialidad_id)
        historias_qs = historias_qs.filter(medico__especialidad_id=especialidad_id)

    if estado:
        citas_qs = citas_qs.filter(estado=estado)

    total_citas = citas_qs.count()
    citas_atendidas = citas_qs.filter(Q(estado="ATENDIDA") | Q(estado="COMPLETADA")).count()
    citas_pendientes = citas_qs.filter(estado="PENDIENTE").count()
    citas_confirmadas = citas_qs.filter(estado="CONFIRMADA").count()
    citas_canceladas = citas_qs.filter(estado="CANCELADA").count()

    total_pacientes = Paciente.objects.count()
    total_medicos = Medico.objects.filter(usuario__is_active=True).count()
    total_historias = historias_qs.count()

    porcentaje_efectividad = round((citas_atendidas / total_citas * 100), 1) if total_citas > 0 else 0

    especialidades_stats = citas_qs.values(
        "medico__especialidad__nombre"
    ).annotate(
        total=Count("id")
    ).order_by("-total")

    medicos_stats = citas_qs.values(
        "medico__id",
        "medico__usuario__first_name",
        "medico__usuario__last_name",
        "medico__usuario__username",
        "medico__especialidad__nombre"
    ).annotate(
        total=Count("id")
    ).order_by("-total")[:10]

    medicos = Medico.objects.select_related("usuario", "especialidad").filter(usuario__is_active=True).order_by("usuario__first_name")

    especialidades = Especialidad.objects.all().order_by("nombre")

    context = {
        "citas": citas_qs.order_by("-fecha", "-hora")[:100],
        "total_citas": total_citas,
        "citas_atendidas": citas_atendidas,
        "citas_pendientes": citas_pendientes,
        "citas_confirmadas": citas_confirmadas,
        "citas_canceladas": citas_canceladas,
        "total_pacientes": total_pacientes,
        "total_medicos": total_medicos,
        "total_historias": total_historias,
        "porcentaje_efectividad": porcentaje_efectividad,
        "especialidades_stats": especialidades_stats,
        "medicos_stats": medicos_stats,
        "medicos": medicos,
        "especialidades": especialidades,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "medico_id": medico_id,
        "especialidad_id": especialidad_id,
        "estado_seleccionado": estado,
    }

    return render(
        request,
        "reportes/index.html",
        context
    )



@login_required
def exportar_citas_csv(request):
    fecha_inicio = request.GET.get("fecha_inicio", "")
    fecha_fin = request.GET.get("fecha_fin", "")
    medico_id = request.GET.get("medico", "")
    especialidad_id = request.GET.get("especialidad", "")
    estado = request.GET.get("estado", "")

    citas_qs = Cita.objects.select_related("paciente", "medico", "medico__usuario", "medico__especialidad").all()

    if fecha_inicio:
        citas_qs = citas_qs.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        citas_qs = citas_qs.filter(fecha__lte=fecha_fin)
    if medico_id:
        citas_qs = citas_qs.filter(medico_id=medico_id)
    if especialidad_id:
        citas_qs = citas_qs.filter(medico__especialidad_id=especialidad_id)
    if estado:
        citas_qs = citas_qs.filter(estado=estado)

    citas_qs = citas_qs.order_by("-fecha", "-hora")

    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = 'attachment; filename="reporte_citas_medicas.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "ID Cita",
        "Fecha",
        "Hora",
        "Paciente",
        "Cédula Paciente",
        "Médico Tratante",
        "Especialidad",
        "Estado",
        "Motivo Consulta",
        "Observaciones"
    ])

    for c in citas_qs:
        nombre_paciente = f"{c.paciente.nombres} {c.paciente.apellidos}"
        nombre_medico = f"Dr. {c.medico.usuario.get_full_name() or c.medico.usuario.username}"
        writer.writerow([
            c.id,
            c.fecha.strftime("%d/%m/%Y"),
            c.hora.strftime("%H:%M"),
            nombre_paciente,
            c.paciente.cedula,
            nombre_medico,
            c.medico.especialidad.nombre,
            c.get_estado_display() if hasattr(c, "get_estado_display") else c.estado,
            c.motivo,
            c.observaciones or ""
        ])

    return response


@login_required
def exportar_historias_csv(request):
    fecha_inicio = request.GET.get("fecha_inicio", "")
    fecha_fin = request.GET.get("fecha_fin", "")
    medico_id = request.GET.get("medico", "")
    especialidad_id = request.GET.get("especialidad", "")

    historias_qs = HistorialMedico.objects.select_related("paciente", "medico", "medico__usuario", "medico__especialidad").all()

    if fecha_inicio:
        historias_qs = historias_qs.filter(fecha__date__gte=fecha_inicio)
    if fecha_fin:
        historias_qs = historias_qs.filter(fecha__date__lte=fecha_fin)
    if medico_id:
        historias_qs = historias_qs.filter(medico_id=medico_id)
    if especialidad_id:
        historias_qs = historias_qs.filter(medico__especialidad_id=especialidad_id)

    historias_qs = historias_qs.order_by("-fecha")

    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = 'attachment; filename="reporte_historias_clinicas.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "ID Historia",
        "Fecha Registro",
        "Paciente",
        "Cédula Paciente",
        "Médico Tratante",
        "Especialidad",
        "Diagnóstico",
        "Síntomas",
        "Tratamiento",
        "Observaciones"
    ])

    for h in historias_qs:
        nombre_paciente = f"{h.paciente.nombres} {h.paciente.apellidos}"
        nombre_medico = f"Dr. {h.medico.usuario.get_full_name() or h.medico.usuario.username}"
        writer.writerow([
            h.id,
            h.fecha.strftime("%d/%m/%Y %H:%M"),
            nombre_paciente,
            h.paciente.cedula,
            nombre_medico,
            h.medico.especialidad.nombre,
            h.diagnostico,
            h.sintomas or "",
            h.tratamiento or "",
            h.observaciones or ""
        ])

    return response
