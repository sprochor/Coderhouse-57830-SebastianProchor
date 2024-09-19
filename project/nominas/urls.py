from django.contrib import admin
from django.urls import path, include
from nominas import views

urlpatterns = [
    path("empleado/list", views.empleado_list, name="empleado_list"),
    path("novedad/list", views.novedad_list, name="novedad_list"),
    path("liquidacion/list", views.liquidacion_list, name="liquidacion_list"),
    path("empleado/create", views.empleado_create, name="empleado_create"),
    path("novedad/create", views.novedad_create, name="novedad_create"),
    path("liquidacion/create", views.liquidacion_create, name="liquidacion_create"),
]
