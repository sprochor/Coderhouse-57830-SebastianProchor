from django import forms
from django.core.exceptions import ValidationError
from .models import Empleado, Novedad, Liquidacion
import re
from datetime import datetime

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = "__all__"
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        pk = self.instance.pk  # Obtiene el ID del empleado que se está actualizando
        
        # Verifica si existe otro empleado con el mismo DNI, excluyendo el actual
        if Empleado.objects.exclude(pk=pk).filter(dni=dni).exists():
            raise ValidationError(f'Ya existe un legajo para un empleado con el DNI {dni}.')
        
        return dni
     
    def clean_fecha_de_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_de_nacimiento')
        if fecha_nacimiento is None:
            raise ValidationError("La fecha de nacimiento es obligatoria.")
        return fecha_nacimiento
    
    def clean_fecha_de_ingreso(self):
        fecha_ingreso = self.cleaned_data.get('fecha_de_ingreso')
        if fecha_ingreso is None:
            raise ValidationError("La fecha de ingreso es obligatoria.")
        return fecha_ingreso

class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        empleado = cleaned_data.get('empleado')
        fecha = cleaned_data.get('fecha')

        if empleado and fecha:
            if Novedad.objects.filter(empleado=empleado, fecha=fecha).exists():
                raise forms.ValidationError("Ya existe una novedad para este legajo en la misma fecha.")
            
class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = ['empleado', 'periodo', 'fecha_pago']
        widgets = {'fecha_pago': forms.DateInput(attrs={'type': 'date'})}
    
    def clean_periodo(self):
        periodo = self.cleaned_data.get('periodo')

        # Verificar si el periodo sigue el formato mm-aaaa usando una expresión regular
        if not re.match(r'^\d{2}-\d{4}$', str(periodo)):
            raise ValidationError('El periodo debe cargarse en el formato mm-aaaa')

        return periodo
    
    def clean(self):
        cleaned_data = super().clean()
        empleado = cleaned_data.get('empleado')
        periodo = cleaned_data.get('periodo')

        # Verificar si el empleado tiene fecha de egreso
        if empleado.fecha_de_egreso:
            # Convertir el periodo en una fecha de tipo datetime para poder compararlo con fecha_de_egreso
            try:
                periodo_date = datetime.strptime(f'01-{periodo}', '%d-%m-%Y').date()  # Agregamos el día para que sea una fecha válida
            except ValueError:
                raise ValidationError(f'El formato del periodo {periodo} es inválido.')

            # Comparar solo si fecha_de_egreso no es None
            if empleado.fecha_de_egreso < periodo_date:
                raise ValidationError(f'El empleado {empleado} ya no estaba activo en el periodo {periodo}.')
        
        # Verificar si ya existe una liquidación para este empleado en el mismo periodo
        if Liquidacion.objects.filter(empleado=empleado, periodo=periodo).exists():
            raise ValidationError(f'Ya existe una liquidación para {empleado} en el periodo {periodo}.')
        
        return cleaned_data