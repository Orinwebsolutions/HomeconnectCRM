from django.core.management.base import BaseCommand
from leads.models import LeadSource, LeadStatus

class Command(BaseCommand):
    help = 'Seeds the database with data for LeadSource'

    def handle(self, *args, **kwargs):
        sources = [
            {"name": "Zillow", "description": "Real estate listings platform"},
            {"name": "Realtor.com", "description": "Real estate website for buying and selling properties"},
            {"name": "Google Ads", "description": "Paid advertisements through Google search and display network"},
            {"name": "Facebook Ads", "description": "Paid advertisements through Facebook and Instagram"},
            {"name": "Company Landing Page", "description": "Landing page dedicated to a specific service or property"},
        ]
        
        for source in sources:
            lead_source, created = LeadSource.objects.get_or_create(name=source['name'], description=source['description'])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created LeadSource: {lead_source.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'LeadSource already exists: {lead_source.name}'))
         
                
        lead_status = [
            {"name": "new", "description": "Lead is newly created"},
            {"name": "assigned", "description": "Assigned to agent"},
            {"name": "unassigned", "description": "Unassigned from agent"},
            {"name": "Closed", "description": "Lead is no longer being pursued"},
            {"name": "Won", "description": "Unassigned from agent"},
            {"name": "Lost", "description": "Lead has been lost"},
        ]
        
        for lead_state in lead_status:
            state_source, created = LeadStatus.objects.get_or_create(name=lead_state['name'], description=lead_state['description'])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created lead status: {state_source.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Lead status already exists: {state_source.name}'))
