from pyexpat.errors import messages
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from products.models import Product
from .forms import CartAddForm, CouponApplyForm
from .cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from products.forms import CommentCreateForm
from .models import Order, OrderItem, DiscountCode
from django.http import HttpResponse, JsonResponse
import json
import requests
import datetime


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


class CreateOrderView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.cart = Cart(request)
        if not self.cart.get_total_price():
            return render(request, 'orders/cart.html', {'cart': self.cart})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        order = Order.objects.create(user=request.user)
        for item in self.cart:
            OrderItem.objects.create(product=item['product'], order=order, quantity=item['quantity'])
        self.cart.clear()
        return redirect('orders:order_detail', order.id)


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order})


# sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8000/cart/verify/'


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        request.session['order_id'] = {
            'order_id': order.id
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    # در صورت موفقیت، تغییر مسیر به صفحه پرداخت زرین پال
                    startpay_url = ZP_API_STARTPAY + str(response['Authority'])
                    return redirect(startpay_url)
                else:
                    return JsonResponse({
                        'status': False,
                        'code': str(response.get('Status'))
                    })
            return JsonResponse({
                'status': False,
                'code': response.status_code
            })
        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})


class OrderPayVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        if request.GET.get('Status') != 'OK':
            # پرداخت لغو شده؛ کاربر را به صفحه مناسب هدایت یا یک پیام مناسب نمایش دهید.
            messages.warning(request, 'فرایند پرداخت سفارش لغو شد.', 'danger')
            return redirect('orders:order_list')

        order = get_object_or_404(Order, id=request.session['order_id']['order_id'])
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Authority": request.GET['Authority'],
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                # return JsonResponse({'status': True, 'RefID': response['RefID']})
                order.paid = True
                order.save()
                del request.session['order_id']
                return redirect('home:home_page')
            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return JsonResponse({'response': response})


class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        orders = request.user.orders.all()
        return render(request, 'orders/user-orders.html', context={'orders': orders})


class OrderDetailView(LoginRequiredMixin, View):
    form = CouponApplyForm
    template = 'orders/order-detail.html'

    def setup(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, id=kwargs['order_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, order_id):
        return render(request, self.template, {'form': self.form, 'order': self.order})

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = DiscountCode.objects.get(code__exact=code, valid_from__lt=now, valid_to__gt=now, active=True)
            except DiscountCode.DoesNotExist:
                messages.error(request, 'این کد تخفیف نامعتبر است', 'danger')
                return redirect(reverse('orders:order_detail', args=(order_id,)))
            self.order.discount = coupon.discount_percentage
            self.order.save()
        return render(request, self.template, {'form': self.form, 'order': self.order})

class OrderDeleteView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        orders = request.user.orders.all()
        messages.success(request, 'سفارش با موفقیت حذف شد', 'success')
        return render(request, 'orders/user-orders.html', context={'orders': orders})
