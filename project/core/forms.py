from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)  # Añadir campo para el avatar

    class Meta:
        model = User  
        fields = ('username', 'first_name', 'last_name', 'email')  


