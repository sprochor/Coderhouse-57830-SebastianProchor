from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include
from nominas import views
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('login', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('nominas/', include('nominas.urls', namespace='nominas')),
]
