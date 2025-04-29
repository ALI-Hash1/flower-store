from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, label='', widget=forms.NumberInput(attrs={
        'class': 'form-control quantity-input',
        'placeholder': 'Quantity'
    }), )


class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=5)
