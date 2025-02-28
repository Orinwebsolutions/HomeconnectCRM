from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from leads.models import Agent

class Command(BaseCommand):
    help = 'Seed sample agents data'

    def handle(self, *args, **kwargs):
        users = [
            {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password123', 'name': 'John Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'password123', 'name': 'Jane Smith'},
            {'username': 'alice_jones', 'email': 'alice@example.com', 'password': 'password123', 'name': 'Alice Jones'},
            {'username': 'bob_brown', 'email': 'bob@example.com', 'password': 'password123', 'name': 'Bob Brown'},
        ]

        for user_data in users:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            agent = Agent.objects.create(
                user=user,
                name=user_data['name']
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully created agent {agent.name}"))
