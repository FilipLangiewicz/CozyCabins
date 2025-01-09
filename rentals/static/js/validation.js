document.getElementById('booking-form').addEventListener('submit', function(event) {
    let isValid = true;
    let errorMessage = '';

    // Get the values of form fields
    const startDate = document.getElementById('id_start_date').value;
    const endDate = document.getElementById('id_end_date').value;
    const guestName = document.getElementById('id_guest_name').value;
    const selectedCabin = document.getElementById('id_cabin').value;

    // Check if all fields are filled
    if (!startDate || !endDate || !guestName || !selectedCabin) {
        isValid = false;
        errorMessage = 'All fields are required! Please select a cabin.';
    }

    // Check if start date is before end date
    if (new Date(startDate) >= new Date(endDate)) {
        isValid = false;
        errorMessage = 'Start date must be before end date!';
    }

    // Check if start date and end date are not in the past
    const today = new Date();
    const startDateObj = new Date(startDate);
    const endDateObj = new Date(endDate);

    if (startDateObj < today) {
        isValid = false;
        errorMessage = 'Start date cannot be in the past!';
    }

    if (endDateObj < today) {
        isValid = false;
        errorMessage = 'End date cannot be in the past!';
    }

    if (!isValid) {
        alert(errorMessage);
        event.preventDefault();
    }
});
