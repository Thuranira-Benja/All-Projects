from django.http import JsonResponse
from .mpesa import lipa_na_mpesa_online

def stk_push_payment(request):
    # For now we hardcode your phone number for testing:
    phone_number = "254745626529"  # Your Safaricom number (Kenya format: 2547...)
    amount = 1  # Test with KES 1

    response = lipa_na_mpesa_online(phone_number, amount)
    return JsonResponse(response)
