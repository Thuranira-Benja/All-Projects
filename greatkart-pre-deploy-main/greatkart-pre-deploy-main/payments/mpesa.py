import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64
import os
from decouple import config

# Load MPESA credentials from .env
MPESA_ENVIRONMENT = config('MPESA_ENVIRONMENT')
MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = config('MPESA_SHORTCODE')
MPESA_PASSKEY = config('MPESA_PASSKEY')
MPESA_CALLBACK_URL = config('MPESA_CALLBACK_URL')

def get_access_token():
    if MPESA_ENVIRONMENT == 'sandbox':
        oauth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    else:
        oauth_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(oauth_url, auth=HTTPBasicAuth(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    r.raise_for_status()
    access_token = r.json().get('access_token')
    return access_token

def lipa_na_mpesa_online(phone_number, amount):
    access_token = get_access_token()

    if MPESA_ENVIRONMENT == 'sandbox':
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    else:
        api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = MPESA_SHORTCODE + MPESA_PASSKEY + timestamp
    encoded_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_payload = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": encoded_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": MPESA_CALLBACK_URL,
        "AccountReference": "OrderPayment",
        "TransactionDesc": "Order Payment"
    }

    response = requests.post(api_url, json=request_payload, headers=headers)
    return response.json()
