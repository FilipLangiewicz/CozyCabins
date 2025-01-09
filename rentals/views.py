from django.shortcuts import render, redirect
from .models import Cabin, Booking
from .forms import BookingForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import json
import xlwt
from django.http import HttpResponse
from django.shortcuts import get_list_or_404


def about(request):
    return render(request, 'rentals/about.html')

@login_required
def book_cabin(request):
    cabin_id = request.GET.get('cabin_id')
    selected_cabin = None
    if cabin_id:
        try:
            selected_cabin = Cabin.objects.get(pk=cabin_id)
        except Cabin.DoesNotExist:
            selected_cabin = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('your_bookings')
    else:
        form = BookingForm()
    cabins = Cabin.objects.all()
    return render(request, 'rentals/book_cabin.html', {'form': form, 'cabins': cabins, 'selected_cabin': selected_cabin})

def index(request):
    cabins = Cabin.objects.all()
    return render(request, 'rentals/index.html', {'cabins': cabins})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            domain = get_current_site(request).domain
            activation_url = f"http://{domain}/activate/{uid}/{token}/"

            subject = "Activate your account"
            message = render_to_string("registration/activation_email.html", {
                'user': user,
                'activation_url': activation_url,
            })

            send_mail(subject, message, 'no-reply@cozycabins.com', [user.email])
            return redirect('email_verification')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def email_verification(request):
    return render(request, 'registration/email_verification.html')

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            messages.success(request, 'Your account has been activated!')
            return redirect('index')
        else:
            messages.error(request, 'Activation link is invalid or expired.')
            return redirect('index')
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('index')

@login_required
def your_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'rentals/your_bookings.html', {'bookings': bookings})

def download_bookings(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    format = request.GET.get("format", "json").lower()
    bookings = Booking.objects.filter(user=user)

    data = []
    for booking in bookings:
        data.append({
            'cabin': booking.cabin.name,
            'start_date': booking.start_date.isoformat(),
            'end_date': booking.end_date.isoformat(),
            'total_nights': int(booking.total_nights()),  
            'price_per_night': float(booking.cabin.price_per_night),
            'total_price': float(booking.total_price()),
        })

    if format == 'json':
        response = HttpResponse(json.dumps(data, indent=4), content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename="bookings.json"'
        return response

    elif format == "xls":
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="bookings.xls"'

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Bookings")

        # Header row
        columns = ["Cabin", "Start Date", "End Date", "Total Nights", "Price per Night", "Total Price"]
        for col_num, column_title in enumerate(columns):
            ws.write(0, col_num, column_title)

        # Data rows
        for row_num, booking in enumerate(bookings, start=1):
            ws.write(row_num, 0, booking.cabin.name)
            ws.write(row_num, 1, booking.start_date.strftime("%Y-%m-%d"))
            ws.write(row_num, 2, booking.end_date.strftime("%Y-%m-%d"))
            ws.write(row_num, 3, booking.total_nights())
            ws.write(row_num, 4, str(booking.cabin.price_per_night))
            ws.write(row_num, 5, str(booking.total_price()))

        wb.save(response)
        return response

    elif format == "xml":
        response = HttpResponse(content_type="application/xml")
        response["Content-Disposition"] = 'attachment; filename="bookings.xml"'

        response.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        response.write("<bookings>\n")
        for booking in bookings:
            response.write("  <booking>\n")
            response.write(f"    <cabin>{booking.cabin.name}</cabin>\n")
            response.write(f"    <start_date>{booking.start_date}</start_date>\n")
            response.write(f"    <end_date>{booking.end_date}</end_date>\n")
            response.write(f"    <total_nights>{booking.total_nights()}</total_nights>\n")
            response.write(f"    <price_per_night>{booking.cabin.price_per_night}</price_per_night>\n")
            response.write(f"    <total_price>{booking.total_price()}</total_price>\n")
            response.write("  </booking>\n")
        response.write("</bookings>\n")
        return response

    return HttpResponse("Invalid format", status=400)