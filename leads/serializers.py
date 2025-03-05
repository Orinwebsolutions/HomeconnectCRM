import re
from django.core.validators import EmailValidator
from rest_framework import serializers
from .models import Lead
from agents.models import Agent
from leads.models import LeadSource, LeadStatus
from property.models import Property


LEAD_TRANSITIONS = {
    "new": ["assigned"],
    "unassigned": ["assigned"],
    "assigned": ["won", "lost"],
    "won": ["reservation"],
    "reservation": ["reserved"],
    "reserved": ["Legal finalize", "assigned"],
    "Legal finalize": ["complete"],
    "complete": ["closed"],
    "closed": ["closed"]
}

class LeadSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[EmailValidator(message="Invalid email format.")])
    class Meta:
        model = Lead
        fields = '__all__'
    
    
    def create(self, validated_data):
        # Remove the fields that should not be set by the user
        validated_data.pop('status', None)
        validated_data.pop('assigned_to', None)
        
        # Create the lead instance
        return super().create(validated_data)
    
    
    def update(self, instance, validated_data):
        validated_data.pop('property', None)  # Remove 'property' from validated_data if it exists
        
        # This is validate stop skipping status 
        current_status = instance.status.name.strip().lower()
        status_id = validated_data.get('status')
        new_status = LeadStatus.objects.filter(id=status_id.id).first()

        # Validate status transition only if the status is changing
        if status_id and new_status != current_status and LeadStatus.objects.filter(id=status_id.id).exists():
            allowed_transitions = LEAD_TRANSITIONS.get(current_status, [])

            if new_status.name.strip().lower() not in allowed_transitions:
                raise serializers.ValidationError(f"Invalid transition: Cannot move from {current_status} to {new_status.name}. Can switch to {allowed_transitions}")
        
        for key, value in validated_data.items():
            setattr(instance, key, value)  # Update only allowed fields
        instance.save()
        return instance
    

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
    
    
    def validate_property(self, value):
        if not Property.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid property ID")
        return value