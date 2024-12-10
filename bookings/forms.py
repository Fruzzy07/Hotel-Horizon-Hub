from django import forms
from .models import Hotel, Room, Customer, Booking, Pricing, Report
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Hotel Form
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'owner']

# Room Form
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'name', 'room_type', 'capacity', 'price', 'is_available']

# Customer Form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

# Booking Form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer', 'room', 'check_in_date', 'check_out_date']

    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),  # Показываем все комнаты, не зависимо от их доступности
        widget=forms.Select(attrs={'class': 'room-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Сортируем комнаты, например, по имени или типу
        self.fields['room'].queryset = Room.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if room and check_in_date and check_out_date:
            # Проверка на пересечение дат бронирования для комнаты
            overlapping_bookings = Booking.objects.filter(
                room=room,
                check_in_date__lt=check_out_date,  # Если новый check-in до существующего check-out
                check_out_date__gt=check_in_date  # И новый check-out после существующего check-in
            )
            if overlapping_bookings.exists():
                raise forms.ValidationError("This room is already booked for the selected dates.")

        return cleaned_data


# Pricing Form
class PricingForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = ['room_type', 'season', 'price']

# Report Form
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['hotel', 'report_type']
