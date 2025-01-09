from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register, logout_view
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('book/', views.book_cabin, name='book_cabin'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset_password/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('reset_password_done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('email_verification/', views.email_verification, name='email_verification'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('your_bookings/', views.your_bookings, name='your_bookings'),
    path("download_bookings/", views.download_bookings, name="download_bookings"),

]