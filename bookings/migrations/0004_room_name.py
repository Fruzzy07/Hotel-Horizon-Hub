# Generated by Django 4.0.1 on 2024-12-10 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_customuser_alter_hotel_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(default='Room', max_length=50),
        ),
    ]
