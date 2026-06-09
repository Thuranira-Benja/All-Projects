from rest_framework import serializers
from .models import BursaryApplication

class BursaryApplicationSerializer(serializers.ModelSerializer):
    applicant_username = serializers.CharField(source='applicant.username', read_only=True)

    class Meta:
        model = BursaryApplication
        fields = [
            'id', 'applicant_username', 'student_name', 'school_name',
            'amount_requested', 'status', 'mpesa_receipt_number', 'created_at'
        ]
        read_only_fields = ['status', 'mpesa_receipt_number']