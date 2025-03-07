from rest_framework import serializers
from .models import Property
from leads.models import Lead
from property.models import Reservation 
        
        
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        
    
    def create(self, validated_data):
        # Remove the fields that should not be set by the user
        validated_data.pop('reservation', None)
        
        # Create the Property instance
        return super().create(validated_data)   
    
class ReservationSerializer(serializers.ModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all())
    class Meta:
        model = Reservation
        fields = '__all__'       