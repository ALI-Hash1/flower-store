from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm


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
            raise ValidationError("your confirmation password does not match")
        return cd

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        # بررسی شروع شماره با 09
        if not phone.startswith('09'):
            raise ValidationError("the phone number must start with 09")

        user = User.objects.filter(phone_number=phone)
        if user:
            raise ValidationError('this phone number has already been registered')
        return phone


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11, widget=forms.TextInput(attrs={
        'class': 'form-control',  # Bootstrap class for styling
        'placeholder': 'Enter your phone number',
        'style': 'font-size: 1.2rem;',  # Larger font size
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',  # Bootstrap class for styling
        'placeholder': 'Enter your password',
        'style': 'font-size: 1.2rem;',  # Larger font size
    }), label='Password')


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your new email address',
        'style': 'margin-bottom: 15px; border-radius: 8px;'
    }),
        label="Email Address")


class ChangePhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your phone number',
        'style': 'border-radius: 8px; border: 1px solid #6a994e; padding: 10px; font-size: 1rem;',
    }), )

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        # بررسی شروع شماره با 09
        if not phone.startswith('09'):
            raise ValidationError("شماره تلفن باید با 09 شروع شود")

        return phone


class PhoneVerifyCodeForm(forms.Form):
    code = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control code-input',
            'style': 'width: 60px; height: 60px; padding: 10px; font-size: 1.5rem; text-align: center; border-radius: 8px; border: 2px solid #6a994e;',
            'maxlength': '4',
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
        }),
        label="",
        required=True
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your current password',
            'style': 'margin-bottom: 15px; border-radius: 8px;'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your new password',
            'style': 'margin-bottom: 15px; border-radius: 8px;'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your new password',
            'style': 'margin-bottom: 15px; border-radius: 8px;'
        })


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'style': 'border-radius: 8px; border: 1px solid #6a994e; padding: 10px; font-size: 1rem;',
        })
    )
