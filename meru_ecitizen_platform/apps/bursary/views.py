import requests
import base64
from datetime import datetime
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from .models import BursaryApplication
from .serializers import BursaryApplicationSerializer

# Simplified M-Pesa STK Push logic
def initiate_stk_push(phone_number, amount, account_reference, transaction_desc):
    # Implementation from the first response can be used here.
    # For brevity, we'll just mock the success case.
    # This is where you would call the Daraja API.
    print(f"MOCK STK PUSH: To {phone_number} for KES {amount}")
    # In a real scenario, the CheckoutRequestID is returned from the API call.
    return {"ResponseCode": "0", "CheckoutRequestID": "ws_CO_MOCK_1234567890"}

class BursaryApplicationViewSet(viewsets.ModelViewSet):
    queryset = BursaryApplication.objects.all()
    serializer_class = BursaryApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BursaryApplication.objects.filter(applicant=self.request.user)

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    @action(detail=True, methods=['post'], url_path='initiate-payment')
    def initiate_payment(self, request, pk=None):
        application = self.get_object()
        processing_fee = 1 # KES 1 for testing
        phone_number = request.user.phone_number
        if not phone_number:
            return Response({"error": "User does not have a phone number."}, status=status.HTTP_400_BAD_REQUEST)

        response_data = initiate_stk_push(
            phone_number=phone_number,
            amount=processing_fee,
            account_reference=f"BURSARY_{application.id}",
            transaction_desc="Bursary Application Fee"
        )

        if response_data and response_data.get('ResponseCode') == '0':
            application.mpesa_checkout_request_id = response_data['CheckoutRequestID']
            application.save()
            return Response({"message": "STK Push initiated. Please check your phone."}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to initiate M-Pesa payment."}, status=status.HTTP_400_BAD_REQUEST)


class MpesaCallbackView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # This is a dummy callback handler.
        print("M-Pesa Callback Received:", request.data)
        # In a real app, you would parse the request.data, find the application
        # via CheckoutRequestID, and update its status.
        return Response(status=status.HTTP_200_OK)