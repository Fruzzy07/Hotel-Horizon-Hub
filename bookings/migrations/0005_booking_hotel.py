# Generated by Django 4.0.1 on 2024-12-10 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='bookings.hotel'),
        ),
    ]
