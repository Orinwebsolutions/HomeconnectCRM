from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Reservation(models.Model):
    name = models.CharField(max_length=50)
    legal_note = models.TextField(blank=True)
    reservation_fee = models.FloatField(default=0.0)
    contract_signed = models.BooleanField(default=False)
    expected_close_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Property(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    price = models.FloatField(default=0.0)
    is_sale = models.BooleanField(default=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name