from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from property.models import Property, Reservation
from leads.models import Lead, LeadStatus
from rest_framework.response import Response
from rest_framework import status
from .serializers import PropertySerializer, ReservationSerializer

# API view for creating a property
@api_view(['POST'])
def create_property(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API view for creating a reservation
@api_view(['POST'])
def create_reservation(request, pk):
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({"error": "property not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    data['property'] = property.id
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        lead_id = serializer.data.get("lead")
        if update_status('reservation', {"lead": lead_id}):
            
            return Response(data, status=status.HTTP_201_CREATED)
                
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API view for making reserve
@api_view(['POST'])
def create_reserved(request, pk, rpk):
    try:
        property_obj = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        reservation = Reservation.objects.get(pk=rpk)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data = { 'lead' : reservation.lead_id}
    if update_status('reserved', data):

        return Response(data, status=status.HTTP_201_CREATED)
    
    return Response({"error": "Failed to update status"}, status=status.HTTP_400_BAD_REQUEST)


def update_status(status_to_update, data):
    lead_id = data.get("lead")  # Ensure correct key access
    if not lead_id:
        return False

    try:
        lead = Lead.objects.get(id=lead_id)
        new_status = LeadStatus.objects.get(name=status_to_update)
        lead.status = new_status
        lead.save()
        return True  # Successfully updated

    except Lead.DoesNotExist:
        return False  # Return False instead of Response

    except LeadStatus.DoesNotExist:
        return False  # Return False instead of Response