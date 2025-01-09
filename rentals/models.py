from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Cabin model, represents a cabin for booking
class Cabin(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cabin_images/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Booking model, stores booking details
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guest_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.guest_name} - {self.cabin.name}"

    def total_nights(self):
        return (self.end_date - self.start_date).days

    def total_price(self):
        return self.total_nights() * self.cabin.price_per_night


# Custom User model with additional fields
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email_confirmed = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name}"
