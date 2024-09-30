from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
from nominas import views as nominas_views

app_name = 'core'

urlpatterns = [
    path('', core_views.index, name="index"),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register/', core_views.Register.as_view(), name='register'),
    path('profile/', core_views.Profile.as_view(), name='profile'),
    path('nominas/', include('nominas.urls', namespace='nominas')),
    path('about/', core_views.abou, name="about"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
