import datetime
import pytz
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm, VerifyCodeForm
from .models import User, OtpCode
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from utils import send_otp_code, AnonymousRequiredMixin
from random import randint
from django.shortcuts import get_object_or_404


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

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید', 'success')
                return redirect('home:home_page')
            messages.error(request, 'شماره تلفن یا رمزعبور اشتباه است', 'danger')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
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
    def test_func(self):
        user_id = self.kwargs.get('user_id')
        return self.request.user.is_authenticated and self.request.user.id == user_id

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'accounts/profile.html', context={'user': user})

