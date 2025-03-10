from django.apps import apps
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Lead
from agents.models import Agent
from leads.models import LeadStatus
from .serializers import LeadSerializer
from rest_framework.permissions import BasePermission


class CanAssignLead(BasePermission):
    def has_permission(self, request, view):
        app_name = apps.get_containing_app_config(view.__module__).name
        permission = f"{app_name}.assign_lead"
        return request.user.has_perm(permission)
    
class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sale Agent').exists()
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()


# API view for retrieving a lead (Function-based view)
@api_view(['GET'])
# @permission_classes([IsAgent])  # Custom permission for assigning leads
def get_lead(request, pk):
    try:
        lead = Lead.objects.get(pk=pk)
        serializer = LeadSerializer(lead)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

# API view for creating a lead
@api_view(['POST'])
def create_lead(request):
    serializer = LeadSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for updating a lead
@api_view(['PUT', 'PATCH'])
def update_lead(request, pk):
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LeadSerializer(lead, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for assigning a lead (custom permission required)
@api_view(['POST'])
@permission_classes([CanAssignLead])
def lead_assign(request, pk):
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # if lead.status.name.lower() not in ["new", "unassigned"]:
    #     return Response({"error": "Lead can only be assigned if its status is 'new' or 'unassigned'."},
    #                     status=status.HTTP_400_BAD_REQUEST)

    assigned_to = request.data.get("assigned_to")

    if not assigned_to or not Agent.objects.filter(id=assigned_to).exists():
        return Response({"error": "Agent ID is incorrect. Please validate and try again."}, 
                        status=status.HTTP_400_BAD_REQUEST)
    if lead.status.name.lower() in ["new", "unassigned"]:    
        lead_status = LeadStatus.objects.filter(name='assigned').first()
        allowed_fields = {"assigned_to": assigned_to, "status" : lead_status.id}
    else:
        allowed_fields = {"assigned_to": assigned_to}

    # allowed_fields = {"assigned_to": assigned_to, "status" : lead_status.id}
    serializer = LeadSerializer(lead, data=allowed_fields, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_status(request, pk):
    # pass
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
    
    new_status = request.data.get("status")
        
    lead_status = LeadStatus.objects.filter(id=new_status).first()

    allowed_fields = {"status" : lead_status.id}
    serializer = LeadSerializer(lead, data=allowed_fields, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)