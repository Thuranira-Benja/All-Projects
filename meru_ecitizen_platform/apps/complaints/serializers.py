from rest_framework import serializers
from .models import Complaint

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id', 'text', 'category', 'confidence_score', 'created_at']
        read_only_fields = ['category', 'confidence_score']