from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
    path('verify/', views.RegisterVerifyCodeView.as_view(), name='user_verify'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='user_profile'),
    path('reset_via_email/', views.PasswordResetView.as_view(), name='user_reset_password_email'),
    path('reset/done/', views.PasswordResetDoneView.as_view(), name='user_reset_password_done'),
    path('confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='user_reset_password_confirm'),
    path('change-password/', views.PasswordChangeView.as_view(), name='user_change_password'),
    path('reset/', views.ResetPasswordView.as_view(), name='user_reset_password'),
    path('reset_via_phone/', views.PasswordResetPhoneView.as_view(), name='user_reset_password_phone'),
    path('reset-phone-done/', views.PasswordResetPhoneDoneView.as_view(), name='user_reset_password_phone_done'),
    path('reset-password-function/', views.PasswordResetFunctionView.as_view(), name='user-reset-password-function')
]
