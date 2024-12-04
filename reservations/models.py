from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_usuario = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=100)
    correo = models.EmailField()

    def registrarse(self):
        pass

    def iniciar_sesion(self):
        pass

    def cerrar_sesion(self):
        pass

    def liberar_mesa(self):
        pass

    def __str__(self):
        return self.nombre_usuario


class Menu(models.Model):
    id_plato = models.AutoField(primary_key=True)
    nombre_plato = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_plato


class Mesa(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    capacidad = models.IntegerField()
    disponibilidad = models.BooleanField(default=True)
    contrasenia = models.CharField(max_length=100, blank=True)

    def esta_disponible(self, fecha):
        hora_inicio = fecha - timedelta(hours=1)
        hora_fin = fecha + timedelta(hours=1)

        return not Reserva.objects.filter(
            mesa=self,
            fecha__range=(hora_inicio, hora_fin),
            estado=True
        ).exists()

    def __str__(self):
        return f"Mesa {self.id_mesa} - Capacidad: {self.capacidad}"


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    plato = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    reserva = models.ForeignKey(
        'Reserva', on_delete=models.CASCADE, related_name='pedidos', null=True)

    def agregar_plato(self):
        pass

    def eliminar_plato(self):
        pass

    def precio_total(self):
        return self.plato.precio * self.cantidad

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.plato} (x{self.cantidad})"


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.BooleanField(default=True)

    def cancelar_reserva(self):
        self.estado = False
        self.save()

    def precio_total(self):
        return sum(pedido.precio_total() for pedido in self.pedidos.all())

    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.cliente}"


class Admin(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def agregar_plato(self):
        pass

    def eliminar_plato(self):
        pass

    def cambiar_disponibilidad(self):
        pass

    def __str__(self):
        return f"Admin - {self.usuario}"
