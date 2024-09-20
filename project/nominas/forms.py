from django import forms
from django.core.exceptions import ValidationError
from .models import Empleado, Novedad, Liquidacion
import re

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = "__all__"

class NovedadForm(forms.ModelForm):  
    class Meta:
        model = Novedad
        fields = "__all__"

class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = ['empleado', 'periodo', 'fecha_pago']
    
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

        # Verificar si ya existe una liquidación para el mismo empleado y periodo
        if Liquidacion.objects.filter(empleado=empleado, periodo=periodo).exists():
            raise ValidationError(f'Ya existe una liquidación para {empleado} en el periodo {periodo}.')
        
        return cleaned_data
