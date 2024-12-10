from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions
from .models import Hotel, Room, Customer, Booking, Pricing, Report
from .forms import HotelForm, RoomForm, CustomerForm, BookingForm, PricingForm, ReportForm
from .serializers import HotelSerializer, RoomSerializer, CustomerSerializer, BookingSerializer, PricingSerializer, ReportSerializer
from .forms import CustomUserCreationForm
from .permissions import IsCustomerUser, IsManagerOrAdmin
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # После успешной регистрации перенаправить на страницу логина
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
# Hotel Views (HTML)
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'bookings/hotel_list.html', {'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.room_set.all()  # Assuming the reverse relation is set
    return render(request, 'bookings/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})

def hotel_create(request):
    if request.user.role not in ['manager', 'admin']:
        return HttpResponseForbidden("You don't have permission to create a hotel.")

    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'bookings/hotel_create.html', {'form': form})

# Room Views (HTML)
# views.py
def room_list(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    rooms = hotel.rooms.all()  # using the 'rooms' related_name defined above
    return render(request, 'bookings/room_list.html', {'hotel': hotel, 'rooms': rooms})

def room_create(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # Only allow managers or admins to create rooms
    if request.user.role not in ['manager', 'admin']:
        return HttpResponseForbidden("You do not have permission to create a room.")

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel  # Assign the room to the hotel
            room.save()
            return redirect('room_list', hotel_id=hotel.id)
    else:
        form = RoomForm()

    return render(request, 'bookings/room_create.html', {'form': form, 'hotel': hotel})

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'bookings/room_detail.html', {'room': room})

# Customer Views (HTML)
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'bookings/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.user.role == 'manager' or request.user.role == 'admin':
        if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('customer_list')
        else:
            form = CustomerForm()
        return render(request, 'bookings/customer_create.html', {'form': form})
    else:
        return HttpResponseForbidden("You do not have permission to create a customer.")

def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'bookings/customer_detail.html', {'customer': customer})

# Booking Views (HTML)
def booking_list(request):
    # Get the hotel you want to pass to the template, or get all hotels if needed
    hotel = Hotel.objects.first()  # Example: Get the first hotel
    bookings = Booking.objects.all()  # or filter bookings for a specific hotel
    return render(request, 'bookings/booking_list.html', {'bookings': bookings, 'hotel': hotel})


def booking_create(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            room = form.cleaned_data['room']
            booking.hotel = hotel
            booking.save()

            # Обновляем статус доступности комнаты
            booking.update_room_availability()

            return redirect('booking_list')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_create.html', {'form': form, 'hotel': hotel})




def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

# Pricing Views (HTML)
def pricing_list(request):
    pricing = Pricing.objects.all()
    return render(request, 'bookings/pricing_list.html', {'pricing': pricing})

def pricing_create(request):
    if request.method == 'POST':
        form = PricingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pricing_list')
    else:
        form = PricingForm()
    return render(request, 'bookings/pricing_create.html', {'form': form})

def pricing_detail(request, pricing_id):
    pricing = get_object_or_404(Pricing, id=pricing_id)
    return render(request, 'bookings/pricing_detail.html', {'pricing': pricing})

# Report Views (HTML)
def report_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    reports = hotel.reports.all()  # Use 'reports' if you have set 'related_name'
    return render(request, 'bookings/report_list.html', {'reports': reports, 'hotel': hotel})

def report_create(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.hotel = hotel  # Assign the hotel
            report.save()
            return redirect('report_list', hotel_id=hotel.id)
    else:
        form = ReportForm()
    return render(request, 'bookings/report_create.html', {'form': form, 'hotel': hotel})

def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'bookings/report_detail.html', {'report': report})


# API Views (for DRF)
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

class PricingViewSet(viewsets.ModelViewSet):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == 'list':  # Просмотр свободных номеров
            return [IsCustomerUser()]
        return [IsManagerOrAdmin()]  # Для других действий (например, создание/редактирование)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.action == 'create':  # Разрешение на создание отчета для CustomerUser
            return [IsCustomerUser()]
        return [
            IsManagerOrAdmin()]  # Для других действий (например, редактирование) — доступ менеджерам и администраторам



