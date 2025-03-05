from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from property.models import Property
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API view for making reserve
@api_view(['POST'])
def create_reserved(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)