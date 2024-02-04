import json
import requests
import base64
import hashlib
from django.conf import settings


def make_base64(json_obj):
    json_str = json.dumps(json_obj, separators=(',', ':'))
    return base64.urlsafe_b64encode(bytes(json_str, "utf-8")).decode("utf-8")


def make_hash(input_str):
    m = hashlib.sha256()
    m.update(input_str.encode())
    return m.hexdigest()


def make_request_body(base64_payload):
    request_body = {
        "request": base64_payload
    }
    data_json = json.dumps(request_body)
    return data_json



def Payment( AMOUNT, REDIRECT_URL,  CALLBACK_URL, MOBILE_NUMBER):

    requests_url = f"{settings.PHONEPE_URL}/pg/v1/pay"
    payload = {
        "merchantId":settings.MERCHANT_ID,
        "merchantTransactionId":'MT8530926168102365478',
        "amount":AMOUNT ,
        "merchantUserId":"MUID123",
        "redirectUrl":REDIRECT_URL,
        "redirectMode":"REDIRECT",
        "callbackUrl": CALLBACK_URL,
        "paymentInstrument": {
            "type": "PAY_PAGE"
        },
        "mobileNumber": MOBILE_NUMBER,
    }

    base64_payload = make_base64(payload)
    verification_str = f"{base64_payload}/pg/v1/pay{settings.SALT_KEY}"
    X_VERIFY = make_hash(verification_str) + "###" + settings.SALT_INDEX
    data = make_request_body(base64_payload)

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY":X_VERIFY
    }

    response = requests.post(requests_url,data=data, headers=headers)
    if response.status_code == 200:
        return [True,response.text]
    else:
        response = json.loads(response.text)
        msg = ""
        if response['code'] == "401":
            msg = "Something went wrong"
        else:
            msg = response['message']
        
            return [False,msg,response['code']]