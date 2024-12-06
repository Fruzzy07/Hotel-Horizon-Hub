from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Hotel, Booking
from .serializers import HotelSerializer, BookingSerializer
from ..user.permissions import IsManager, IsAdmin


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, IsManager]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # All authenticated users can book

