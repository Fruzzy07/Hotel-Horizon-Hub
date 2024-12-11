from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import date

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    # Добавьте related_name, чтобы избежать конфликта с встроенными полями User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Измените на уникальное имя
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Измените на уникальное имя
        blank=True
    )


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, default="Unknown Address")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='hotels', null=True, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite')
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=50, default='Room')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.get_room_type_display()} at {self.hotel.name}"



class Customer(models.Model):
    name = models.CharField(max_length=100, default='Anonymous')
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, default='000-000-0000')


    def __str__(self):
        return self.name


class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings', default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def clean(self):
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        )
        if overlapping_bookings.exists():
            raise ValidationError('This room is already booked for the selected dates.')

    def __str__(self):
        return f"Booking by {self.customer.name} for {self.room}"

    def update_room_availability(self):
        if self.check_out_date >= date.today():
            self.room.is_available = False
            self.room.save()
        elif self.check_out_date < date.today():
            self.room.is_available = True
            self.room.save()

    def get_season_price(self):
        # Fetch the room's price for the correct season based on check-in date
        month = self.check_in_date.month
        pricing = Pricing.get_price_for_room_and_season(self.room.room_type, month)
        return pricing.price if pricing else None


class Pricing(models.Model):
    room_type = models.CharField(max_length=20, choices=Room.ROOM_TYPES)
    season = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.room_type} - {self.season} - {self.price}"

    @staticmethod
    def get_season_by_month(month):
        """Returns the season for a given month"""
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    @classmethod
    def get_price_for_room_and_season(cls, room_type, month):
        """Returns the price for a specific room type in a specific season"""
        season = cls.get_season_by_month(month)
        return cls.objects.filter(room_type=room_type, season=season).first()



class Report(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.report_type} - {self.created_at}"

