from django.shortcuts import render, redirect
from .models import Empleado, Liquidacion, Novedad
from .forms import EmpleadoForm, NovedadForm, LiquidacionForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "core/index.html")

@login_required
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

@login_required
def empleado_detail(request, pk: int):
    query = Empleado.objects.get(nro_legajo=pk)
    context = {'object': query}
    return render(request, 'nominas/empleado_detail.html', context)

@login_required
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

@login_required
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

@login_required
def liquidacion_detail(request, pk: int):
    query = Liquidacion.objects.get(id=pk)
    context = {'object': query}
    return render(request, 'nominas/liquidacion_detail.html', context)

@login_required
def empleado_create(request):
    if request.method == "GET":
        form = EmpleadoForm()
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nominas:empleado_list")
    return render(request, "nominas/empleado_form.html", {"form": form})

@login_required
def novedad_create(request):
    if request.method == "GET":
        form = NovedadForm()
    if request.method == "POST":
        form = NovedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nominas:novedad_list")
    return render(request, "nominas/novedad_form.html", {"form": form})

@login_required
def liquidacion_create(request):
    if request.method == "GET":
        form = LiquidacionForm()
    if request.method == "POST":
        form = LiquidacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nominas:liquidacion_list")
    return render(request, "nominas/liquidacion_form.html", {"form": form})

@login_required
def empleado_update(request, pk: int):
    query = Empleado.objects.get(nro_legajo=pk)
    if request.method == "GET":
        form = EmpleadoForm(instance=query)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect("nominas:empleado_list")
    return render(request, "nominas/empleado_form.html", {"form": form})

@login_required
def liquidacion_update(request, pk: int):
    query = Liquidacion.objects.get(id=pk)
    if request.method == "GET":
        form = LiquidacionForm(instance=query)
    if request.method == "POST":
        form = LiquidacionForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect("nominas:liquidacion_list")
    return render(request, "nominas/liquidacion_form.html", {"form": form})

@login_required
def empleado_delete(request, pk: int):
    query = Empleado.objects.get(nro_legajo=pk)
    if request.method == "POST":
        query.delete()
        return redirect("nominas:empleado_list")
    return render(request, 'nominas/empleado_confirm_delete.html', {'object':query})

@login_required
def liquidacion_delete(request, pk: int):
    query = Liquidacion.objects.get(id=pk)
    if request.method == "POST":
        query.delete()
        return redirect("nominas:liquidacion_list")
    return render(request, 'nominas/liquidacion_confirm_delete.html', {'object':query})

@login_required
def novedad_update(request, pk: int):
    query = Novedad.objects.get(id=pk)
    if request.method == "GET":
        form = NovedadForm(instance=query)
    if request.method == "POST":
        form = NovedadForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect("nominas:novedad_list")
    return render(request, "nominas/novedad_form.html", {"form": form})

@login_required
def novedad_delete(request, pk: int):
    query = Novedad.objects.get(id=pk)
    if request.method == "POST":
        query.delete()
        return redirect("nominas:novedad_list")
    return render(request, 'nominas/novedad_confirm_delete.html', {'object':query})

@login_required
def novedad_detail(request, pk: int):
    query = Novedad.objects.get(id=pk)
    context = {'object': query}
    return render(request, 'nominas/novedad_detail.html', context)