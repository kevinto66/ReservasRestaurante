from django.utils import timezone

def get_active_reservations(queryset):
    """
    Filter reservations to show only current and future reservations that are active
    """
    now = timezone.now()
    return queryset.filter(fecha__gte=now, estado=True).order_by('fecha')
