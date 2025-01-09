// Add event listener to form submission
document.getElementById('form-registration').addEventListener('submit', function(event) {
    let isValid = true; // Flag to track if the form is valid
    let errorMessage = ''; // Variable to store error message

    // Get the values of form fields
    const username = document.getElementById('id_username').value;
    const email = document.getElementById('id_email').value;
    const firstName = document.getElementById('id_first_name').value;
    const lastName = document.getElementById('id_last_name').value;
    const dateOfBirth = document.getElementById('id_date_of_birth').value;
    const password1 = document.getElementById('id_password1').value;
    const password2 = document.getElementById('id_password2').value;

    // Check if any field is empty
    if (!username || !email || !firstName || !lastName || !dateOfBirth || !password1 || !password2) {
        isValid = false; // Set form validity to false
        errorMessage = 'All fields are required!'; // Set the error message
    }

    // Validate email format using regex
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address!';
    }

    // Check if passwords match
    if (password1 !== password2) {
        isValid = false;
        errorMessage = 'Passwords do not match!';
    }

    // Validate date of birth: ensure it's not in the future
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    if (birthDate >= today) {
        isValid = false;
        errorMessage = 'Date of birth cannot be in the future!';
    }

    // If form is not valid, show an alert and prevent form submission
    if (!isValid) {
        alert(errorMessage); // Display error message
        event.preventDefault(); // Prevent form submission
    }
});
