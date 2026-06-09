# greatkart/payments/mpesa_utils.py
import requests
import base64
from datetime import datetime
from django.conf import settings

def get_access_token():
    """Get M-Pesa access token"""
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" if settings.MPESA_ENVIRONMENT == 'sandbox' else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    response = requests.get(api_URL, auth=(consumer_key, consumer_secret))
    return response.json().get('access_token')

def generate_password():
    """Generate M-Pesa API password"""
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = f"{shortcode}{passkey}{timestamp}"
    password_bytes = password_str.encode('ascii')
    return base64.b64encode(password_bytes).decode('utf-8'), timestamp

def initiate_stk_push(phone_number, amount, account_reference, description):
    """Initiate STK push to customer's phone"""
    access_token = get_access_token()
    password, timestamp = generate_password()
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": description
    }
    
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" if settings.MPESA_ENVIRONMENT == 'sandbox' else "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()