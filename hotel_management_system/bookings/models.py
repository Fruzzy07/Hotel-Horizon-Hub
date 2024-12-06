from django.db import models

from users.models import CustomUser

# from django.contrib.auth.models import CustomUser

class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    MANAGER = 'MANAGER', 'Manager'
    GUEST = 'GUEST', 'Guest'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.GUEST)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rooms_available = models.IntegerField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Booking by {self.customer} at {self.hotel}'
