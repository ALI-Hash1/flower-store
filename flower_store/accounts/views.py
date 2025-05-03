import datetime
import pytz
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm, VerifyCodeForm, ChangeEmailForm, ChangePhoneForm, PhoneVerifyCodeForm, \
    SetNewPasswordForm, CustomPasswordChangeForm
from .models import User, OtpCode
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from utils import send_otp_code, AnonymousRequiredMixin
from random import randint
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


class RegisterView(AnonymousRequiredMixin, View):
    form = RegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = randint(1000, 9999)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['user_register_info'] = {'phone_number': cd['phone_number'], 'password': cd['password1']}
            messages.success(request, 'کد پیامک شده را وارد کنید...', 'success')
            send_otp_code(cd['phone_number'], random_code)
            return redirect('accounts:user_verify')
        return render(request, self.template_name, {'form': form})


class LoginView(AnonymousRequiredMixin, View):
    form = LoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user:
                login(request, user)
                if self.next:
                    return redirect(self.next)
                messages.success(request, 'شما با موفقیت وارد شدید', 'success')
                return redirect('home:home_page')
            messages.error(request, 'شماره تلفن یا رمزعبور اشتباه است', 'danger')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'شما با موفقیت خارج شدید', 'success')
        return redirect('home:home_page')


class RegisterVerifyCodeView(View):
    form = VerifyCodeForm

    def get(self, request):
        return render(request, 'accounts/verify.html', {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user_session = request.session['user_register_info']
            code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                if datetime.datetime.now(tz=pytz.timezone('Asia/Tehran')) <= code_instance.created + datetime.timedelta(
                        minutes=2):
                    User.objects.create_user(phone_number=user_session['phone_number'],
                                             password=user_session['password'])
                    code_instance.delete()
                    messages.success(request, 'you registered.', 'success')
                    return redirect('home:home_page')
                else:
                    messages.error(request, 'the code has expired, please try again...')
                    return redirect('accounts:user_register')
                del request.session['user_register_info']
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return render(request, 'accounts/verify.html', {'form': form})


class ProfileView(UserPassesTestMixin, View):
    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=kwargs['user_id'])
        self.password_form = CustomPasswordChangeForm(user=self.user)
        return super().setup(request, *args, **kwargs)

    def test_func(self):
        user_id = self.kwargs.get('user_id')
        return self.request.user.is_authenticated and self.request.user.id == user_id

    def get(self, request, user_id):
        email_form = ChangeEmailForm
        return render(request, 'accounts/profile.html',
                      context={'user': self.user, 'form': self.password_form, 'email_form': email_form})

    def post(self, request, user_id):
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.user.email = cd['email']
            self.user.save()
            messages.success(request, 'email successfully saved', 'success')
            return redirect(reverse('accounts:user_profile', args=(self.user.id,)))
        messages.error(request, 'email is invalid, try again...', 'danger')
        return render(request, 'accounts/profile.html',
                      context={'user': self.user, 'form': self.password_form, 'email_form': form})


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password-reset-form.html'
    success_url = reverse_lazy('accounts:user_reset_password_done')
    email_template_name = 'accounts/password-reset-email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password-reset-done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirm.html'
    success_url = reverse_lazy('accounts:user_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'رمز عبور شما با موفقیت تغییر پیدا کرد.')
        return response


class PasswordChangeView(LoginRequiredMixin, View):
    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت.')
            return redirect(reverse('accounts:user_profile', args=(request.user.id,)))
        messages.error(request, 'لطفاً اطلاعات صحیح وارد کنید.')
        return render(request, 'accounts/profile.html', context={'user': request.user, 'form': form})


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'accounts/reset-password.html')


class PasswordResetPhoneView(View):
    form = ChangePhoneForm
    template = 'accounts/password-reset-phone.html'

    def get(self, request):
        return render(request, self.template, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(phone_number=cd['phone_number'])
            if not user.exists():
                messages.success(request, 'کد پیامک شده را وارد کنید...', 'success')
                return redirect('accounts:user_reset_password_phone_done')
            random_code = randint(1000, 9999)
            exist_code = OtpCode.objects.get(phone_number=cd['phone_number'])
            if exist_code:
                exist_code.delete()
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['user_reset_phone'] = {'phone_number': cd['phone_number']}
            messages.success(request, 'کد پیامک شده را وارد کنید...', 'success')
            send_otp_code(cd['phone_number'], random_code)
            return redirect('accounts:user_reset_password_phone_done')
        return render(request, self.template, {'form': form})


class PasswordResetPhoneDoneView(View):
    form = PhoneVerifyCodeForm
    template = 'accounts/password-reset-phone-done.html'

    def get(self, request):
        return render(request, self.template, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user_session = request.session['user_reset_phone']
            try:
                code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
            except OtpCode.DoesNotExist:
                messages.error(request, "این کد اشتباه است, دوباره تلاش کنید...", "danger")
                return redirect('accounts:user_reset_password_phone')
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                if datetime.datetime.now(tz=pytz.timezone('Asia/Tehran')) <= code_instance.created + datetime.timedelta(
                        minutes=2):
                    request.session['key'] = {'sample_key': 'abc'}
                    messages.success(request, 'رمز عبور خود را تغییر دهید...', 'success')
                    return redirect('accounts:user-reset-password-function')
                else:
                    messages.error(request, 'کد ارسالی منقضی شده است, لطفا دوباره تلاش کنید...', "danger")
                    del request.session['user_reset_phone']
                    return redirect('accounts:user_reset_password_phone')
            else:
                del request.session['user_reset_phone']
                messages.error(request, 'کد ارسالی شما اشتباه بود, دوباره تلاش کنید...', 'danger')
                return redirect('accounts:user_reset_password_phone')
        return render(request, self.template, {'form': form})


class PasswordResetFunctionView(View):
    form = SetNewPasswordForm
    template = 'accounts/phone-change-password.html'

    def get(self, request):
        if not request.session.get('key'):
            messages.error(request, "دسترسی غیرمجاز. لطفاً ابتدا درخواست ریست رمز عبور را انجام دهید")
            return redirect('accounts:user_reset_password_phone')
        return render(request, self.template, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_session = request.session['user_reset_phone']
            user = User.objects.get(phone_number=user_session['phone_number'])
            user.set_password(cd['new_password1'])
            user.save()
            messages.success(self.request, "رمز عبور شما با موفقیت تغییر یافت. لطفاً با رمز عبور جدید وارد شوید.",
                             "success")
            del request.session['user_reset_phone']
            del request.session['key']
            return redirect('accounts:user_login')
        return render(request, self.template, {'form': form})
