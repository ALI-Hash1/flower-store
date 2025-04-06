from kavenegar import *
from django.shortcuts import redirect
from django.db import models


def send_otp_code(phone_number, code):
    api = KavenegarAPI('474A334554647259417064556F6644516C376E447877496E70497A7A744171474F7833556D457A496556593D')
    params = {'sender': '2000660110', 'receptor': phone_number, 'message': f'{code} کد تایید شما: '}
    response = api.sms_send(params)
    print(response)


class AnonymousRequiredMixin:
    redirect_url = 'home:home_page'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class SEOMixin(models.Model):
    keyword = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        abstract = True
