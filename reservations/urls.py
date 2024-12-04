from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('reserva/', views.hacer_reserva, name='hacer_reserva'),
    path('cancelar-reserva/<int:reserva_id>/',
         views.cancelar_reserva, name='cancelar_reserva'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('gestionar-menu/', views.gestionar_menu, name='gestionar_menu'),
    path('gestionar-mesas/', views.gestionar_mesas, name='gestionar_mesas'),
    path('toggle-menu/<int:plato_id>/', views.toggle_menu_disponibilidad,
         name='toggle_menu_disponibilidad'),
    path('toggle-mesa/<int:mesa_id>/', views.toggle_mesa_disponibilidad,
         name='toggle_mesa_disponibilidad'),
]
