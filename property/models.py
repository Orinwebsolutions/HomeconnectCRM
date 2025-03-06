from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
    
class Property(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    price = models.FloatField(default=0.0)
    is_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Reservation(models.Model):
    name = models.CharField(max_length=50)
    legal_note = models.TextField(blank=True)
    reservation_fee = models.FloatField(default=0.0)
    contract_signed = models.BooleanField(default=False)
    expected_close_date = models.DateTimeField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reservations", null=True)
    lead = models.ForeignKey("leads.lead", on_delete=models.CASCADE, related_name="reservations_lead", null=True)
    # lead = models.ForeignKey(Leads,.... This line change to we receive "initialized module 'leads.models' (most likely due to a circular import)"
    # So mitigate above error. Use a string-based reference ("app.ModelName") => "leads.lead" instead of direct imports.
    # "leads.Lead" tells Django not to import Lead immediately but to resolve it after all models are loaded.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name