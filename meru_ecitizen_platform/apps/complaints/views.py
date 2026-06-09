import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
from .models import Complaint
from .serializers import ComplaintSerializer

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def perform_create(self, serializer):
        complaint_text = serializer.validated_data.get('text')
        
        try:
            # Proxy the request to the FastAPI ML service
            ml_service_url = f"{settings.ML_API_BASE_URL}/complaints/classify"
            response = requests.post(ml_service_url, json={"text": complaint_text}, timeout=5)
            response.raise_for_status()
            
            ml_data = response.json()
            category = ml_data.get('category', 'OTHER').upper()
            confidence = ml_data.get('confidence')
            
            serializer.save(
                submitted_by=self.request.user,
                category=category,
                confidence_score=confidence
            )
        except requests.exceptions.RequestException as e:
            # If ML service fails, save as 'OTHER' and log the error
            print(f"Could not connect to ML service: {e}")
            serializer.save(
                submitted_by=self.request.user,
                category=Complaint.Category.OTHER,
                confidence_score=0.0
            )