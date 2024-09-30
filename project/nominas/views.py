from django.shortcuts import render, redirect
from .models import Empleado, Liquidacion, Novedad
from .forms import EmpleadoForm, NovedadForm, LiquidacionForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import calendar
from django.shortcuts import render, get_object_or_404

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
def liquidacion_detail(request, pk):
    liquidacion = get_object_or_404(Liquidacion, pk=pk)

    # Lógica para calcular los datos de liquidación
    sueldo_diario = liquidacion.empleado.sueldo / 30 if liquidacion.empleado.sueldo > 0 else 0
    print(f'Sueldo: {liquidacion.empleado.sueldo}, Sueldo Diario: {sueldo_diario}')

    # Días de ausencia cargados como "Novedad" para el empleado en el período
    ausencias = Novedad.objects.filter(
        empleado=liquidacion.empleado,
        tipo_novedad='AS',
        fecha__year=int(liquidacion.periodo.split('-')[1]),
        fecha__month=int(liquidacion.periodo.split('-')[0])
    ).count()

    # Obtener fecha de ingreso
    fecha_ingreso = liquidacion.empleado.fecha_de_ingreso
    dias_trabajados = 30  # Siempre 30 días como base

    if fecha_ingreso:
        ultimo_dia_mes = calendar.monthrange(fecha_ingreso.year, fecha_ingreso.month)[1]
        dias_trabajados = ultimo_dia_mes - fecha_ingreso.day + 1  # +1 para incluir el día de ingreso

    # Días trabajados después de restar ausencias
    dias_trabajados -= ausencias  # Resta las ausencias directamente
    print(f'Ausencias: {ausencias}, Días Trabajados: {dias_trabajados}')

    # Calcular sueldo bruto y descuentos
    sueldo_bruto = dias_trabajados * sueldo_diario if sueldo_diario > 0 else 0
    jubilacion = sueldo_bruto * -Decimal('0.11')
    obra_social = sueldo_bruto * -Decimal('0.03')
    ley_19032 = sueldo_bruto * -Decimal('0.03')

    # Sueldo neto
    sueldo_neto = (sueldo_diario * dias_trabajados) - (jubilacion + obra_social + ley_19032)

    # Contexto para la plantilla
    context = {
        'object': liquidacion,
        'descuento_jubilacion': jubilacion,
        'descuento_obra_social': obra_social,
        'descuento_ley_19032': ley_19032,
        'dias_trabajados': dias_trabajados, 
        'monto_resta_ingreso': (dias_trabajados + ausencias - 30) * sueldo_diario,  # Lógica para el monto de ingreso
        'monto_resta_ausencias': ausencias * -sueldo_diario,  # Lógica para el monto de ausencias
    }

    return render(request, 'nominas/liquidacion_detail.html', context)

@login_required
def empleado_form(request):
    if request.method == "GET":
        form = EmpleadoForm()
    elif request.method == "POST":
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("nominas:empleado_list") 
    return render(request, "nominas/empleado_form.html", {"form": form})


@login_required
def novedad_form(request):
    if request.method == "GET":
        form = NovedadForm()
    if request.method == "POST":
        form = NovedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nominas:novedad_list")
    return render(request, "nominas/novedad_form.html", {"form": form})

@login_required
def liquidacion_form(request):
    if request.method == "POST":
        form = LiquidacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nominas:liquidacion_list")
    else:
        form = LiquidacionForm()

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