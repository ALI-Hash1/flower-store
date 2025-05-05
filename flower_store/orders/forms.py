from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, label='', widget=forms.NumberInput(attrs={
        'class': 'form-control quantity-input',
        'placeholder': 'Quantity'
    }), )


class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=5, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter discount code',
        'style': 'border-radius: 8px; border: 1px solid #6a994e; padding: 10px; font-size: 1rem; margin-bottom: 15px;',
    }),
                           label="")
