from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


class RegisterView(View):
    form = RegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(phone_number=cd['phone_number'], password=cd['password1'])
            messages.success(request, 'ثبت‌نام شما با موفقیت انجام شد! لطفاً وارد شوید', 'success')
            return redirect('home:home_page')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
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
