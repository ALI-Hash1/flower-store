from django import forms
from django.forms import PasswordInput
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
from django.contrib import messages


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        passwd1 = cd.get('password1')
        passwd2 = cd.get('password2')
        if passwd1 and passwd2 and passwd1 != passwd2:
            raise ValidationError("passwords don't match")

        return passwd2

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
    phone_number = forms.CharField(max_length=11, min_length=11, widget=forms.TextInput(attrs={
        'class': 'form-control',  # Bootstrap class for styling
        'placeholder': 'Enter your phone number',
        'style': 'font-size: 1.2rem;',  # Larger font size
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',  # Bootstrap class for styling
        'placeholder': 'Enter your password',
        'style': 'font-size: 1.2rem;',  # Larger font size
    }), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',  # Bootstrap class for styling
        'placeholder': 'Confirm your password',
        'style': 'font-size: 1.2rem;',  # Larger font size
    }), label='Confirm Password')

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("رمز عبور تایید شده شما مطابقت ندارد")
        return cd

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


class ChangeEmailForm(forms.Form):
    email = forms.EmailField()


class ChangePhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        # بررسی شروع شماره با 09
        if not phone.startswith('09'):
            raise ValidationError("شماره تلفن باید با 09 شروع شود")

        return phone


class PhoneVerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="رمز عبور جدید",
        min_length=8,
        help_text="رمز عبور باید حداقل 8 کاراکتر داشته باشد."
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="تکرار رمز عبور جدید",
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('new_password1')
        pwd2 = cleaned_data.get('new_password2')

        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError("رمزهای عبور وارد شده مطابقت ندارند.")
        return cleaned_data
