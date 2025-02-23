from kavenegar import *


def send_otp_code(phone_number, code):
    api = KavenegarAPI('474A334554647259417064556F6644516C376E447877496E70497A7A744171474F7833556D457A496556593D')
    params = {'sender': '2000660110', 'receptor': '09932775742', 'message': f'{code} کد تایید شما: '}
    response = api.sms_send(params)
