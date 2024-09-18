from django.shortcuts import render
from .models import Empleado, Liquidacion, Novedad
from .forms import EmpleadoForm, NovedadForm, LiquidacionForm
from django.shortcuts import redirect

def index(request):
    return render(request, "nominas/index.html")

def empleado_list(request):
    query = Empleado.objects.all()
    context = {"object_list": query}
    return render(request, "nominas/empleado_list.html", context)

def novedad_list(request):
    query = Novedad.objects.all()
    context = {"object_list": query}
    return render(request, "nominas/novedad_list.html", context)

def liquidacion_list(request):
    query = Liquidacion.objects.all()
    context = {"object_list": query}
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