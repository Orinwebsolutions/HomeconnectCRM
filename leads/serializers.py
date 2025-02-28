import re
from django.core.validators import EmailValidator
from rest_framework import serializers
from .models import Lead
from agents.models import Agent
from leads.models import LeadSource

class LeadSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[EmailValidator(message="Invalid email format.")])
    class Meta:
        model = Lead
        fields = '__all__'
    
    
    def create(self, validated_data):
        # Remove the fields that should not be set by the user
        validated_data.pop('property', None)
        validated_data.pop('status', None)
        validated_data.pop('assigned_to', None)
        
        # Create the lead instance
        return super().create(validated_data)
    

    def validate_source(self, value):
        if not LeadSource.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid lead source.")
        return value
    

    def validate_phone(self, value):
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value


    def validate_assigned_to(self, value):
        if not Agent.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid agent ID.")
        return value