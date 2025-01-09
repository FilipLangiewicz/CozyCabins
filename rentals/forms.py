from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# Form for booking a cabin
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['cabin', 'start_date', 'end_date', 'guest_name']


# Custom user creation form, extending Django's built-in UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    # Adding custom field for the user's date of birth
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2')
