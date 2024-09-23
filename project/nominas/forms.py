from django import forms
from django.core.exceptions import ValidationError
from .models import Empleado, Novedad, Liquidacion
import re

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

class NovedadForm(forms.ModelForm):  
    class Meta:
        model = Novedad
        fields = "__all__"
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'})}

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

        if empleado.fecha_de_egreso and empleado.fecha_de_egreso < periodo:
            raise ValidationError(f'El empleado {empleado} ya no estaba activo en el periodo {periodo}.')

        if Liquidacion.objects.filter(empleado=empleado, periodo=periodo).exists():
            raise ValidationError(f'Ya existe una liquidación para {empleado} en el periodo {periodo}.')
        
        return cleaned_data
