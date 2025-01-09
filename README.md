# CozyCabins: Vacation Rental Management Platform

CozyCabins is a web application designed to streamline the process of managing vacation cabin rentals. The platform provides users with the ability to browse available cabins, book stays, and manage their bookings. Additionally, administrators can monitor bookings and manage cabins effectively.

## Features

- **User-Friendly Booking System**: Allows users to browse and book cabins based on availability.
- **Authentication and Authorization**:
  - User registration with email verification.
  - Secure login/logout functionality.
- **Booking Management**: 
  - Users can view and manage their bookings.
  - Export bookings in JSON, XML, or Excel formats.
- **Admin Features**: Admins can manage cabins and monitor user bookings.
- **Responsive Design**: Optimized for both desktop and mobile use.

---

## Technologies Used

- **Backend**: Django 5.1.4
- **Frontend**: HTML, CSS (Django Templates)
- **Database**: SQLite (default, can be swapped with PostgreSQL/MySQL for production)
- **Other Tools**:
  - `xlwt` for exporting bookings to Excel.
  - `json` and `xml` modules for data serialization.

---

### Usage
- Register a new user:
  - Sign up using the registration form.
  - Check your email for the activation link to verify your account.
- Book a Cabin:
  - Browse the available cabins on the homepage.
  - Select a cabin and choose your desired dates.
  - Confirm your booking.
- View and Manage Bookings:
  - Go to the "Your Bookings" page to view and manage existing bookings.
  - Export your bookings in your preferred format (JSON, XML, or Excel).
- Admin Dashboard:
  - Log in as a superuser to access the Django admin interface.
  - Manage cabins, users, and bookings.
