from django import forms
from django.forms import PasswordInput
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User

from .models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("password don't match")

        return cd['password1']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\"../password/\">this form</a>")

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password')


class RegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("رمز عبور تایید شده شما مطابقت ندارد")

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        # بررسی شروع شماره با 09
        if not phone.startswith('09'):
            raise ValidationError("شماره تلفن باید با 09 شروع شود")

        user = User.objects.filter(phone_number=phone)
        if user:
            raise ValidationError('این شماره تلفن قبلا ثبت شده است')
        return phone


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()
