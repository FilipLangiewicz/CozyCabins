from django.contrib import admin
from rentals.models import CustomUser

from .models import Cabin, Booking

admin.site.register(Cabin)
admin.site.register(Booking)
admin.site.register(CustomUser)