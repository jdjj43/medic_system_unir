from django.urls import path

from .views import (
    panel_reportes,
    exportar_citas_csv,
    exportar_historias_csv,
)


urlpatterns = [

    path(
        "",
        panel_reportes,
        name="panel_reportes"
    ),

    path(
        "exportar-citas-csv/",
        exportar_citas_csv,
        name="exportar_citas_csv"
    ),

    path(
        "exportar-historias-csv/",
        exportar_historias_csv,
        name="exportar_historias_csv"
    ),

]
