from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Cabin, Booking
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )
        self.image = SimpleUploadedFile("dsakademik.jpg", b"file_content", content_type="image/jpeg")

        self.cabin = Cabin.objects.create(
            name="Cozy Cabin",
            description="A very cozy cabin.",
            price_per_night=100.00,
            available=True,
            image = self.image
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/index.html')
        self.assertContains(response, "Cozy Cabin")

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/about.html')

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'date_of_birth': '2000-01-01'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

    def test_book_cabin_view_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('book_cabin'), {
            'cabin': self.cabin.id,
            'start_date': date.today() + timedelta(days=1),
            'end_date': date.today() + timedelta(days=3),
            'guest_name': 'Test Guest'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful booking
        self.assertEqual(Booking.objects.count(), 1)

    def test_book_cabin_view_unauthenticated(self):
        response = self.client.get(reverse('book_cabin'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_your_bookings_view(self):
        self.client.login(username="testuser", password="testpassword")

        booking = Booking.objects.create(
            user=self.user,
            cabin=self.cabin,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            guest_name="Test Guest"
        )

        response = self.client.get(reverse('your_bookings'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/your_bookings.html')

        self.assertEqual(len(response.context['bookings']), 1)
        self.assertEqual(response.context['bookings'][0], booking)

    def test_email_verification_view(self):
        response = self.client.get(reverse('email_verification'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/email_verification.html')

    def test_activate_account_view(self):
        token = 'dummy-token'
        uid = 'dummy-uid'
        response = self.client.get(reverse('activate_account', args=[uid, token]))
        self.assertEqual(response.status_code, 302)
