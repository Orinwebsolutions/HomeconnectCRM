from django.core.management.base import BaseCommand
from leads.models import LeadSource, LeadStatus, Property

class Command(BaseCommand):
    help = 'Seeds the database with data for Property'

    def handle(self, *args, **kwargs):
        sources = [
            {"name": "Shangri-la apartment", "description": "3 bed rooms, 2 attached bathrooms, 1 servant bathroom", "address" : "Colombo", "price" : 1200000 },
            {"name": "One galleface apartment", "description": "2 bed rooms, 2 attached bathrooms, 1 servant bathroom", "address" : "Colombo", "price" : 1500000 },
            {"name": "Luxury apartment for sell", "description": "3 bed rooms, 3 attached bathrooms, 1 servant bathroom", "address" : "Nugegoda", "price" : 1100000 },
            {"name": "Two storey house for sell", "description": "4 bed rooms, 3 attached bathrooms", "address" : "Gampaha", "price" : 900000 },
            {"name": "Land for sell", "description": "40 perch land for sell", "address" : "Kalutara", "price" : 1575000 },
            {"name": "Land for sell in Hanwella", "description": "50 perch land for sell", "address" : "Hanwella", "price" : 7500000 },
            {"name": "Land for sell Nuwara Eliya", "description": "1 Acer for sell", "address" : "Kalutara", "price" : 2000000 },
            {"name": "Land for sell Avissawella", "description": "40 perch land for sell", "address" : "Avissawella", "price" : 5500000 },
        ]
        
        
        for source in sources:
            lead_source, created = Property.objects.get_or_create(name=source['name'], description=source['description'], address=source['address'], price=source['price'])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Property: {lead_source.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Property already exists: {lead_source.name}'))
         
