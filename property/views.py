from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from property.models import Property, Reservation
from leads.models import Lead, LeadStatus
from leads.serializers import LeadSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import PropertySerializer, ReservationSerializer
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)

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
def create_reservation(request):
    lead_id = request.data.get("lead")
    try:
        current_lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if Reservation.objects.filter(lead_id=lead_id, status="1").exists():
    
        return Response({"error": f"Reservation already exist on this lead id {lead_id}"}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data
    data['property'] = current_lead.property_id # Always set lead property to reservation
    data['status'] = '1' # Always set pending when create reservation
    if update_status('reservation', {"lead": lead_id}) == True:
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": f"Failed to update lead id#{lead_id} status"}, status=status.HTTP_400_BAD_REQUEST) 

# API view for making reserve
@api_view(['POST'])
def create_reserved(request, pk):   
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data = { 'lead' : reservation.lead_id}
    if update_status('reserved', data):
        allowed_fields = {'status': '3'} 
        serializer = ReservationSerializer(reservation, data=allowed_fields, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Failed to update status"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def cancel_reservation(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if reservation.lead.status.name.lower() not in ["reservation"]:
        return Response({"error": "Lead only can cancel if its current status is 'reservation'."},
                        status=status.HTTP_400_BAD_REQUEST)
        
    lead_status = LeadStatus.objects.filter(name='assigned').first()

    # ToDo add message for cancel reason
    allowed_fields = {"status" : lead_status.id}
    serializer = LeadSerializer(reservation.lead, data=allowed_fields, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        allowed_fields = {"status" : '2'} # change reservation status cancel
        reservation_serializer = ReservationSerializer(reservation, data=allowed_fields, partial=True)
        if reservation_serializer.is_valid():
            reservation_serializer.save()
            # logger.info('reservation_serializer saved')
            
            return Response(reservation_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": "Updated Lead status but not able update reservation status."},status=status.HTTP_400_BAD_REQUEST)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_status(status_to_update, data):
    lead_id = data.get("lead")  # Ensure correct key access
    if not lead_id:
        return False
    
    try:
        new_status = LeadStatus.objects.get(name=status_to_update)
        allowed_fields = {"status" : new_status.id}
        lead = Lead.objects.get(id=lead_id)
        serializer = LeadSerializer(lead, data=allowed_fields, partial=True)
        if serializer.is_valid():
            serializer.save()
            return True
        return False
    
    except Lead.DoesNotExist:
        return False  # Return False instead of Response

    except LeadStatus.DoesNotExist:
        return False  # Return False instead of Response