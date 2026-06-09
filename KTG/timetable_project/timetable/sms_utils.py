import africastalking
import os

# Initialize with your sandbox credentials
USERNAME = "sandbox"  # Or your production username
API_KEY = "atsk_ef5ee3e70f4feb7a26d1cce0dc5b9ee9d2c9ab0ac6efab9b4e160c32bc064bceae42360c"  # Replace with your key

africastalking.initialize(USERNAME, API_KEY)
sms = africastalking.SMS

def send_sms_notification(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        return response
    except Exception as e:
        print(f"Error sending SMS to {phone_number}: {e}")
        return None
