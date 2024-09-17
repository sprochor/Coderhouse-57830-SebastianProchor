from django.db import models
from datetime import date

class Empleado(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('P', 'Pasivo'),
    ]

    MOD_CONTRATACION_CHOICES = [
        ('T', 'Temporal'),
        ('P', 'Permanente'),
    ]

    nro_legajo = models.AutoField(primary_key=True)
    nombre_empleado = models.CharField(max_length=50)
    apellido_empleado = models.CharField(max_length=50)
    sexo_empleado = models.CharField(max_length=1, choices=SEXO_CHOICES)  # Elección entre Masculino y Femenino
    celular = models.CharField(max_length=30, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    fecha_de_nacimiento = models.DateField()
    fecha_de_ingreso = models.DateField()
    fecha_de_egreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)  # Elección entre Activo y Pasivo
    nacionalidad = models.CharField(max_length=100)  # Campo para ingresar el país a mano
    mod_contratacion = models.CharField(max_length=1, choices=MOD_CONTRATACION_CHOICES, blank=True, null=True)  # Elección entre Temporal y Permanente
    puesto = models.CharField(max_length=100)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)  # Sueldo en formato de moneda

    def __str__(self):
        return f'{self.nombre_empleado} {self.apellido_empleado} (Legajo: {self.nro_legajo}) - {self.puesto}'


class Novedad(models.Model):
    TIPO_NOVEDAD_CHOICES = [
        ('AS', 'Ausencia'),
        ('LI', 'Licencia'),
    ]
    
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)
    tipo_novedad = models.CharField(max_length=2, choices=TIPO_NOVEDAD_CHOICES)  # Tipo de novedad
    descripcion = models.CharField(max_length=255, blank=True, null=True)  # Descripción adicional (opcional)
    fecha = models.DateField()
    fecha_creacion = models.DateField(auto_now_add=True)  # Fecha de creación automática
    comentarios = models.TextField(blank=True, null=True)  # Comentarios adicionales (opcional)

    def __str__(self):
        return f'Novedad de {self.empleado} - {self.get_tipo_novedad_display()} ({self.fecha})'
    
class Liquidacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        LIQUIDADO = 'LIQUIDADO', 'Liquidado'
        PAGADO  = 'PAGADO', 'Pagado'

    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)  
    periodo = models.CharField(max_length=7)  # Ejemplo: "09-2024" (mes y año)
    fecha_liquidacion = models.DateField(default=date.today)  # Fecha de la liquidación
    total_horas_extras_50 = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)  # Total de horas extras al 50%
    total_horas_extras_100 = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)  # Total de horas extras al 100%
    total_dias_ausencia = models.IntegerField(default=0)  # Total de días de ausencia
    total_liquidacion = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_pago = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)

    def __str__(self):
        return f'Liquidación {self.periodo} - {self.empleado.nombre_empleado} {self.empleado.apellido_empleado} (Legajo: {self.empleado.nro_legajo})'