# store/mpesa_utils.py

import requests
import base64
from datetime import datetime
import os

def get_access_token():
    consumer_key = os.getenv('MPESA_CONSUMER_KEY')
    consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    
    if response.status_code == 200:
        return response.json()['access_token']
    return None

def format_phone_number(phone):
    if phone.startswith("07"):
        return "254" + phone[1:]
    if phone.startswith("+254"):
        return phone[1:]
    return phone

def lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc):
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to get access token"}

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = os.getenv('MPESA_SHORTCODE')
    passkey = os.getenv('MPESA_PASSKEY')
    
    # Generate password
    data_to_encode = shortcode + passkey + timestamp
    online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    # IMPORTANT: Update this with your ngrok URL for testing
    callback_url = "https://your-ngrok-url.io/mpesa/callback/"

    payload = {
        "BusinessShortCode": shortcode,
        "Password": online_password,
        "Timestamp": timestamp,
        "TransactionType": os.getenv('MPESA_TRANSACTION_TYPE'),
        "Amount": str(int(amount)), # Amount must be an integer
        "PartyA": format_phone_number(phone_number),
        "PartyB": shortcode,
        "PhoneNumber": format_phone_number(phone_number),
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()