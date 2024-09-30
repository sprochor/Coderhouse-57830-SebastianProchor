from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from decimal import Decimal
from django import forms
import calendar

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
    dni = models.CharField(max_length=8)
    sexo_empleado = models.CharField(max_length=1, choices=SEXO_CHOICES)  # Elección entre Masculino y Femenino
    celular = models.CharField(max_length=30, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    fecha_de_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    fecha_de_ingreso = models.DateField()
    fecha_de_egreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)  # Elección entre Activo y Pasivo
    nacionalidad = models.CharField(max_length=100)  # Campo para ingresar el país a mano
    mod_contratacion = models.CharField(max_length=1, choices=MOD_CONTRATACION_CHOICES, blank=True, null=True)  # Elección entre Temporal y Permanente
    puesto = models.CharField(max_length=100)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    avatar = models.ImageField(upload_to='avatares', blank=True, null=True)

    def clean(self):
        # Validar que la fecha de ingreso no sea posterior a la fecha de egreso
        if self.fecha_de_egreso and self.fecha_de_ingreso > self.fecha_de_egreso:
            raise ValidationError('La fecha de ingreso no puede ser posterior a la fecha de egreso.')
        
        # Validar que el empleado sea mayor de 18 años
        today = date.today()
        age = today.year - self.fecha_de_nacimiento.year - ((today.month, today.day) < (self.fecha_de_nacimiento.month, self.fecha_de_nacimiento.day))
        if age < 18:
            raise ValidationError('El empleado debe ser mayor de 18 años.')
        
        return super().clean()

    def get_fecha_de_nacimiento_display(self):
        if self.fecha_de_nacimiento:
            return self.fecha_de_nacimiento.strftime("%d/%m/%Y")
        return "Fecha no disponible"

    def __str__(self):
        return f'{self.nombre_empleado} {self.apellido_empleado} (Legajo: {self.nro_legajo}) - {self.puesto}'


class Novedad(models.Model):
    TIPO_NOVEDAD_CHOICES = [
        ('AS', 'Ausencia'),
        ('LI', 'Licencia'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_novedad = models.CharField(max_length=2, choices=TIPO_NOVEDAD_CHOICES)  # Tipo de novedad
    descripcion = models.CharField(max_length=255, blank=True, null=True)  # Descripción adicional (opcional)
    fecha = models.DateField()
    fecha_creacion = models.DateField(auto_now_add=True)  # Fecha de creación automática
    comentarios = models.TextField(blank=True, null=True)  # Comentarios adicionales (opcional)

    def __str__(self):
        return f'Novedad de {self.empleado} - {self.get_tipo_novedad_display()} ({self.fecha})'


class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ['empleado', 'tipo_novedad', 'descripcion', 'fecha', 'comentarios']  # Campos a incluir

    def clean(self):
        cleaned_data = super().clean()
        empleado = cleaned_data.get('empleado')
        fecha = cleaned_data.get('fecha')

        if empleado and fecha:
            if Novedad.objects.filter(empleado=empleado, fecha=fecha).exists():
                raise forms.ValidationError("Ya existe una novedad para este legajo en la misma fecha.")


class Liquidacion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=7)  # Ejemplo: "09-2024" (mes y año)
    fecha_liquidacion = models.DateField(default=date.today)
    total_dias_ausencia = models.IntegerField(default=0)
    total_liquidacion = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_pago = models.DateField()

    def calcular_total_liquidacion(self):
        # Sueldo diario (siempre basado en 30 días)
        sueldo_diario = self.empleado.sueldo / 30 if self.empleado.sueldo > 0 else 0
        print(f'Sueldo: {self.empleado.sueldo}, Sueldo Diario: {sueldo_diario}')

        # Días de ausencia cargados como "Novedad" para el empleado en el período
        ausencias = Novedad.objects.filter(
            empleado=self.empleado,
            tipo_novedad='AS',
            fecha__year=int(self.periodo.split('-')[1]),
            fecha__month=int(self.periodo.split('-')[0])
        ).count()

        # Obtener fecha de ingreso
        fecha_ingreso = self.empleado.fecha_de_ingreso

        # Inicializar días trabajados
        dias_trabajados = 30  # Siempre 30 días como base

        ultimo_dia_mes = calendar.monthrange(fecha_ingreso.year, fecha_ingreso.month)[1]
        dias_trabajados = ultimo_dia_mes - fecha_ingreso.day + 1  # Sumamos 1 para incluir el día de ingreso

        # Días trabajados después de restar ausencias
        dias_trabajados -= ausencias
        print(f'Ausencias: {ausencias}, Días Trabajados: {dias_trabajados}')

        # Calcular el sueldo bruto descontando los días no trabajados
        sueldo_bruto = dias_trabajados * sueldo_diario if sueldo_diario > 0 else 0
        print(f'Sueldo Bruto: {sueldo_bruto}')

        # Aplicar descuentos
        jubilacion = sueldo_bruto * Decimal('0.11')  # 11% de descuento para jubilación
        ley_19032 = sueldo_bruto * Decimal('0.03')  # 3% para ley 19032
        obra_social = sueldo_bruto * Decimal('0.03')  # 3% para obra social

        print(f'Jubilación: {jubilacion}, Ley 19032: {ley_19032}, Obra Social: {obra_social}')

        # Sueldo neto después de los descuentos
        sueldo_neto = sueldo_bruto - (jubilacion + ley_19032 + obra_social)
        print(f'Sueldo Neto: {sueldo_neto}')

        return sueldo_neto

    def save(self, *args, **kwargs):
        # Calculamos la liquidación antes de guardarla
        self.total_liquidacion = self.calcular_total_liquidacion()

        # Guardamos el total de ausencias en el campo correspondiente
        self.total_dias_ausencia = Novedad.objects.filter(
            empleado=self.empleado,
            tipo_novedad='AS',
            fecha__year=int(self.periodo.split('-')[1]),
            fecha__month=int(self.periodo.split('-')[0])
        ).count()

        super().save(*args, **kwargs)

    def __str__(self):
        sueldo_diario = self.empleado.sueldo / 30 if self.empleado.sueldo > 0 else 0
        sueldo_neto = self.total_liquidacion
        return (
            f'Liquidación {self.periodo} - {self.empleado.nombre_empleado} {self.empleado.apellido_empleado} '
            f'(Legajo: {self.empleado.nro_legajo}) - Días trabajados: {30 - self.total_dias_ausencia} - '
            f'Sueldo bruto: {self.empleado.sueldo:.2f} - Ausencias: {self.total_dias_ausencia} - Sueldo neto: {sueldo_neto:.2f}'
        )