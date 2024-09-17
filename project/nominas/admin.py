from django.contrib import admin
from .models import Empleado, Novedad, Liquidacion

class NovedadAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipo_novedad', 'descripcion', 'fecha', 'comentarios', 'fecha_creacion')
    list_filter = ('tipo_novedad', 'empleado')

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nro_legajo', 'nombre_empleado', 'apellido_empleado', 'sexo_empleado', 'estado', 'nacionalidad', 'puesto', 'sueldo')
    search_fields = ('nombre_empleado', 'apellido_empleado', 'nro_legajo')

class LiquidacionAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'periodo', 'fecha_liquidacion', 'total_horas_extras_50', 'total_horas_extras_100', 'total_dias_ausencia', 'total_liquidacion', 'fecha_pago', 'estado')
    list_filter = ('empleado', 'estado', 'periodo')
    search_fields = ('empleado__nombre_empleado', 'empleado__apellido_empleado', 'periodo')

admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Novedad, NovedadAdmin)
admin.site.register(Liquidacion, LiquidacionAdmin)
