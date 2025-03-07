from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
    
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
    class ReservationStatus(models.IntegerChoices):
        PENDING = 1, _('Reservation Pending')
        CANCEL = 2, _('Reservation Cancel')
        FINAL = 3, _('Reservation Final')
        
    name = models.CharField(max_length=50)
    legal_note = models.TextField(blank=True)
    reservation_fee = models.FloatField(default=0.0)
    contract_signed = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=ReservationStatus, default=ReservationStatus.PENDING )
    expected_close_date = models.DateTimeField()
    lead = models.ForeignKey("leads.lead", on_delete=models.CASCADE, related_name="reservations_lead", null=True)
    # lead = models.ForeignKey(Leads,.... This line change to we receive "initialized module 'leads.models' (most likely due to a circular import)"
    # So mitigate above error. Use a string-based reference ("app.ModelName") => "leads.lead" instead of direct imports.
    # "leads.Lead" tells Django not to import Lead immediately but to resolve it after all models are loaded.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name