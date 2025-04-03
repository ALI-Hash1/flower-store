from pyexpat.errors import messages

from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from products.models import Product
from .forms import CartAddForm
from .cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from products.forms import CommentCreateForm


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        # base functionality
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        # miscellaneous information
        comments = product.product_comments.filter(is_reply=False)
        form_class = CommentCreateForm
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
            messages.success(request, 'product added to the cart basket', 'success')
            return redirect('orders:cart')
        return render(request, 'products/product.html', {'product': product, 'comments': comments, 'form': form_class,
                                                         'purchase_form': form})


class CartRemoveView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        return redirect('orders:cart')
