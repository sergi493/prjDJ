
from django.urls import path
from . import views
urlpatterns = [
     path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("vender/", views.vender, name="vender"),
    path("facturas/", views.facturas, name="facturas"),
    path("tickets/", views.tickets, name="tickets"),
    path("devoluciones/", views.tasks, name="devoluciones"),
    path("stock/", views.stock, name="stock"),
     path("create_project/", views.create_project, name="create_project"),
     
]
