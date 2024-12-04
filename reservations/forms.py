from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reserva, Menu, Mesa, Pedido
from django.utils import timezone
from datetime import timedelta


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PedidoFormSet(forms.BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        if not any(form.cleaned_data.get('cantidad', 0) > 0 for form in self.forms):
            raise forms.ValidationError('Debe seleccionar al menos un plato')


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['plato', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'plato': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plato'].queryset = Menu.objects.filter(
            disponibilidad=True)
        for plato in self.fields['plato'].queryset:
            self.fields['plato'].widget.choices.queryset = Menu.objects.filter(
                disponibilidad=True)
            # Add precio as data attribute to each option
            self.fields['plato'].widget.attrs['data-precio'] = plato.precio


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['mesa', 'fecha']
        widgets = {
            'fecha': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mesa'].label = 'Mesa'
        self.fields['fecha'].label = 'Fecha y Hora'

        # Set min date to today and max date to 30 days from now
        now = timezone.now()
        min_date = now.strftime('%Y-%m-%dT%H:%M')
        max_date = (now + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M')

        self.fields['fecha'].widget.attrs.update({
            'min': min_date,
            'max': max_date
        })

    def clean(self):
        cleaned_data = super().clean()
        mesa = cleaned_data.get('mesa')
        fecha = cleaned_data.get('fecha')

        if mesa and fecha:
            # Verificar si hay reservas para la misma mesa en un rango de ±1 hora
            hora_inicio = fecha - timedelta(hours=1)
            hora_fin = fecha + timedelta(hours=1)

            reservas_existentes = Reserva.objects.filter(
                mesa=mesa,
                fecha__range=(hora_inicio, hora_fin),
                estado=True
            )

            if reservas_existentes.exists():
                raise forms.ValidationError(
                    'Esta mesa ya está reservada para este horario. Por favor, elija otro horario o mesa.'
                )


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nombre_plato', 'descripcion', 'precio', 'disponibilidad']
