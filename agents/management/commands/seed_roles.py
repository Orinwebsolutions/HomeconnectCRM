from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from leads.models import Lead

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create roles (groups)
        roles = ["Sale Agent", "Admin"]
        role_groups = {}

        for role_name in roles:
            group, created = Group.objects.get_or_create(name=role_name)
            role_groups[role_name] = group
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created role: {role_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Role already exists: {role_name}'))

        # Define permissions
        content_type = ContentType.objects.get_for_model(Lead) 
        
        permissions = {
            "view_lead": "Can view lead",
            "assign_lead": "Can assign leads",
            "lead_status": "Can change lead status",
        }

        created_permissions = {}

        for codename, name in permissions.items():
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type
            )
            created_permissions[codename] = permission
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created permission: {codename}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Permission already exists: {codename}'))

        # Assign permissions to roles
        role_permissions = {
            "Sale Agent": ["lead_status", "view_lead"],
            "Admin": ["assign_lead", "lead_status", "view_lead"]
        }

        for role_name, permission_codenames in role_permissions.items():
            group = role_groups[role_name]
            for codename in permission_codenames:
                permission = created_permissions[codename]
                group.permissions.add(permission)

            self.stdout.write(self.style.SUCCESS(f'Updated permissions for {role_name}'))