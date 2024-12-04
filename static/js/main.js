// Form Validation
document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // DateTime picker enhancement
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateInputs.forEach(input => {
        // Set min date to today
        const today = new Date();
        const todayStr = today.toISOString().slice(0, 16);
        input.min = todayStr;

        // Set max date to 30 days from now
        const maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 30);
        const maxDateStr = maxDate.toISOString().slice(0, 16);
        input.max = maxDateStr;
    });
});

// Dynamic Table Availability
function updateTableAvailability() {
    const tables = document.querySelectorAll('.table-item');
    const currentTime = new Date();

    tables.forEach(table => {
        const reservationTime = new Date(table.dataset.reservationTime);
        if (reservationTime < currentTime) {
            table.classList.remove('table-reserved');
            table.classList.add('table-available');
        }
    });
}

// Reservation Confirmation
function confirmReservation(reservationId) {
    if (confirm('¿Estás seguro de que deseas confirmar esta reserva?')) {
        // Add AJAX call to backend here
        return true;
    }
    return false;
}

// Menu Item Availability Toggle
function toggleMenuItemAvailability(itemId, available) {
    const menuItem = document.querySelector(`#menu-item-${itemId}`);
    if (menuItem) {
        menuItem.classList.toggle('available', available);
        menuItem.classList.toggle('unavailable', !available);
    }
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function () {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});