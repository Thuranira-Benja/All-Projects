from datetime import date, timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import BusinessPermit
from .serializers import BusinessPermitSerializer
from .tasks import generate_and_save_permit_pdf_task

class BusinessPermitViewSet(viewsets.ModelViewSet):
    queryset = BusinessPermit.objects.all()
    serializer_class = BusinessPermitSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='process-payment')
    def process_payment(self, request, pk=None):
        permit = self.get_object()
        receipt_no = request.data.get('receipt_no')

        if not receipt_no:
            return Response({"error": "Receipt number is required."}, status=status.HTTP_400_BAD_REQUEST)

        permit.status = BusinessPermit.PermitStatus.ACTIVE
        permit.receipt_no = receipt_no
        permit.expiry_date = date.today() + timedelta(days=365)
        permit.save()

        generate_and_save_permit_pdf_task.delay(str(permit.id))
        serializer = self.get_serializer(permit)
        return Response(serializer.data)

# ✅ OUTSIDE the class
@staff_member_required
def dashboard_view(request):
    permits = BusinessPermit.objects.select_related('owner').all().order_by('-issue_date')
    return render(request, 'licensing/dashboard.html', {'permits': permits})
