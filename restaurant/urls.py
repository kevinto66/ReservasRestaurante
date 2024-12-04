from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/reservations/', permanent=True)),
    path('reservations/', include('reservations.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
