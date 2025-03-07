# Generated by Django 5.1.6 on 2025-03-07 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_reservation_lead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='property',
        ),
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[(1, 'Reservation Pending'), (2, 'Reservation Cancel'), (3, 'Reservation Final')], default=1, max_length=2),
        ),
    ]
