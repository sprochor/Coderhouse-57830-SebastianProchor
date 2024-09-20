from django.shortcuts import render, redirect
from .models import Empleado, Liquidacion, Novedad
from .forms import EmpleadoForm, NovedadForm, LiquidacionForm
from django.db.models import Q

def index(request):
    return render(request, "core/index.html")

def empleado_list(request):
    query = request.GET.get("q")
    
    if query:
         empleados = Empleado.objects.filter(
            Q(nombre_empleado__icontains=query) | Q(apellido_empleado__icontains=query)
        )
    else:
        empleados = Empleado.objects.all()
    
    context = {"object_list": empleados}
    return render(request, "nominas/empleado_list.html", context)

def novedad_list(request):
    query = request.GET.get("q")
    
    if query:
        novedades = Novedad.objects.filter(
            Q(empleado__nombre_empleado__icontains=query) | Q(empleado__apellido_empleado__icontains=query)
        )
    else:
        novedades = Novedad.objects.all()
    
    context = {"object_list": novedades}  
    return render(request, "nominas/novedad_list.html", context)

def liquidacion_list(request):
    query = request.GET.get("q")
    
    if query:
        novedades = Liquidacion.objects.filter(
            Q(empleado__nombre_empleado__icontains=query) | Q(empleado__apellido_empleado__icontains=query)
        )
    else:
        novedades = Liquidacion.objects.all()
    
    context = {"object_list": novedades}
    return render(request, "nominas/liquidacion_list.html", context)

def empleado_create(request):
    if request.method == "GET":
        form = EmpleadoForm()
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("empleado_list")
    return render(request, "nominas/empleado_create.html", {"form": form})

def novedad_create(request):
    if request.method == "GET":
        form = NovedadForm()
    if request.method == "POST":
        form = NovedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("novedad_list")
    return render(request, "nominas/novedad_create.html", {"form": form})

def liquidacion_create(request):
    if request.method == "GET":
        form = LiquidacionForm()
    if request.method == "POST":
        form = LiquidacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("liquidacion_list")
    return render(request, "nominas/liquidacion_create.html", {"form": form})