from django.urls import path

from .views import lista_auditoria


urlpatterns = [

    path(
        "lista/",
        lista_auditoria,
        name="lista_auditoria"
    ),

]
