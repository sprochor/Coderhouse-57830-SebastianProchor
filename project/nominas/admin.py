from django.contrib import admin
from .models import Empleado, Novedad, Liquidacion

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nro_legajo', 'nombre_empleado', 'apellido_empleado', 'sueldo')

class NovedadAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipo_novedad', 'fecha')

class LiquidacionAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'periodo', 'total_liquidacion')
    readonly_fields = ('total_liquidacion',)  

admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Novedad, NovedadAdmin)
admin.site.register(Liquidacion, LiquidacionAdmin)

