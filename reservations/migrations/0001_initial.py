# Generated by Django 4.2.7 on 2024-12-01 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id_plato', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_plato', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disponibilidad', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id_mesa', models.AutoField(primary_key=True, serialize=False)),
                ('capacidad', models.IntegerField()),
                ('disponibilidad', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.CharField(max_length=100)),
                ('contrasenia', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id_reserva', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('estado', models.BooleanField(default=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.usuario')),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.mesa')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('plato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.menu')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reservations.usuario')),
            ],
        ),
    ]
