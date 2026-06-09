from rest_framework import serializers
from .models import BusinessPermit

class BusinessPermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPermit
        fields = '__all__'
        read_only_fields = ['id', 'issue_date']
