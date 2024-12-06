from django.db import models

from user.models import Guest


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rooms_available = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    customer = models.ForeignKey(Guest, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Booking by {self.customer} at {self.hotel}'
