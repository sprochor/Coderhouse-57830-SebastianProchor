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
    path('empleado/detail/<int:pk>', views.empleado_detail, name="empleado_detail"),
    path('liquidacion/detail/<int:pk>', views.liquidacion_detail, name="liquidacion_detail"),    
    path('empleado/update/<int:pk>', views.empleado_update, name="empleado_update"),
    path('liquidacion/update/<int:pk>', views.liquidacion_update, name="liquidacion_update"),  
]
