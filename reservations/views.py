from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.forms import modelformset_factory
from django.db import transaction
from .forms import UserRegistrationForm, ReservaForm, MenuForm, PedidoForm, PedidoFormSet
from .models import Reserva, Menu, Mesa, Usuario, Pedido
from django.utils import timezone
from django.contrib.auth.models import User
from .utils import get_active_reservations


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Verificar si ya existe un usuario con el nombre de usuario o el correo
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(
                    request, 'Ya existe una cuenta con ese correo electrónico.')
                return redirect('register')

            # Crear el usuario en el sistema
            user = form.save()

            # Verificar si ya existe un usuario en la tabla 'Usuario' con el mismo 'user_id'
            if not Usuario.objects.filter(user=user).exists():
                # Crear el objeto Usuario solo si no existe
                Usuario.objects.create(
                    user=user,
                    nombre_usuario=user.username,
                    correo=user.email,
                )

            # Loguear al usuario inmediatamente después del registro
            login(request, user)

            # Redirigir al usuario a la página principal después del registro
            messages.success(request, 'Registro exitoso. Bienvenido!')
            # Asegúrate de que 'home' sea el nombre de la URL correcta
            return redirect('home')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        # Get only active and future reservations
        reservas = get_active_reservations(Reserva.objects.filter(cliente=usuario))
        menu = Menu.objects.filter(disponibilidad=True)
        return render(request, 'reservations/home.html', {
            'reservas': reservas,
            'menu': menu
        })
    except Usuario.DoesNotExist:
        messages.error(request, 'Error: Usuario no encontrado')
        return redirect('logout')

@login_required
def hacer_reserva(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        PedidoFormSetFactory = modelformset_factory(
            Pedido,
            form=PedidoForm,
            formset=PedidoFormSet,
            extra=Menu.objects.filter(disponibilidad=True).count()
        )
        
        if request.method == 'POST':
            reserva_form = ReservaForm(request.POST)
            pedido_formset = PedidoFormSetFactory(request.POST, queryset=Pedido.objects.none())
            
            if reserva_form.is_valid() and pedido_formset.is_valid():
                with transaction.atomic():
                    # Crear la reserva
                    reserva = reserva_form.save(commit=False)
                    reserva.cliente = usuario
                    reserva.save()
                    
                    # Crear los pedidos
                    for form in pedido_formset:
                        if form.cleaned_data.get('cantidad', 0) > 0:
                            pedido = form.save(commit=False)
                            pedido.reserva = reserva
                            pedido.save()
                    
                    # Actualizar disponibilidad de la mesa
                    mesa = reserva.mesa
                    mesa.disponibilidad = False
                    mesa.save()
                    
                    messages.success(request, 'Reserva realizada con éxito')
                    return redirect('home')
        else:
            reserva_form = ReservaForm()
            initial = [{'plato': plato} for plato in Menu.objects.filter(disponibilidad=True)]
            pedido_formset = PedidoFormSetFactory(queryset=Pedido.objects.none(), initial=initial)
        
        return render(request, 'reservations/hacer_reserva.html', {
            'reserva_form': reserva_form,
            'pedido_formset': pedido_formset
        })
    except Usuario.DoesNotExist:
        messages.error(request, 'Error: Usuario no encontrado')
        return redirect('home')

@login_required
def cancelar_reserva(request, reserva_id):
    try:
        usuario = Usuario.objects.get(user=request.user)
        reserva = get_object_or_404(Reserva, id_reserva=reserva_id, cliente=usuario)
        
        if not reserva.estado:
            messages.error(request, 'Esta reserva ya está cancelada')
            return redirect('home')
        
        if reserva.fecha < timezone.now():
            messages.error(request, 'No se puede cancelar una reserva pasada')
            return redirect('home')
        
        reserva.cancelar_reserva()
        messages.success(request, 'Reserva cancelada con éxito')
        return redirect('home')
    except Usuario.DoesNotExist:
        messages.error(request, 'Error: Usuario no encontrado')
        return redirect('home')

@login_required
def admin_panel(request):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado')
        return redirect('home')
    
    menu = Menu.objects.all()
    mesas = Mesa.objects.all()
    # Get only active and future reservations for admin panel
    reservas = get_active_reservations(Reserva.objects.all())
    return render(request, 'reservations/admin_panel.html', {
        'menu': menu,
        'mesas': mesas,
        'reservas': reservas
    })

@login_required
def gestionar_menu(request):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado')
        return redirect('home')
    
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato agregado exitosamente')
            return redirect('gestionar_menu')
    else:
        form = MenuForm()
    
    platos = Menu.objects.all()
    return render(request, 'reservations/gestionar_menu.html', {
        'form': form,
        'platos': platos
    })

@login_required
def gestionar_mesas(request):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado')
        return redirect('home')
    
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesa agregada exitosamente')
            return redirect('gestionar_mesas')
    else:
        form = MesaForm()
    
    mesas = Mesa.objects.all()
    return render(request, 'reservations/gestionar_mesas.html', {
        'form': form,
        'mesas': mesas
    })

@login_required
def toggle_menu_disponibilidad(request, plato_id):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado')
        return redirect('home')

    if request.method == 'POST':
        plato = get_object_or_404(Menu, id_plato=plato_id)
        plato.disponibilidad = not plato.disponibilidad
        plato.save()
        messages.success(request, f'Disponibilidad de {plato.nombre_plato} actualizada')

    return redirect('gestionar_menu')


@login_required
def toggle_mesa_disponibilidad(request, mesa_id):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado')
        return redirect('home')

    if request.method == 'POST':
        mesa = get_object_or_404(Mesa, id_mesa=mesa_id)
        mesa.disponibilidad = not mesa.disponibilidad
        mesa.save()
        messages.success(request, f'Estado de la mesa {mesa.id_mesa} actualizado')

    return redirect('gestionar_mesas')
