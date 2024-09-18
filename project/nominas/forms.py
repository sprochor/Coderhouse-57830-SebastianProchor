from django import forms
from .models import Empleado, Novedad, Liquidacion

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