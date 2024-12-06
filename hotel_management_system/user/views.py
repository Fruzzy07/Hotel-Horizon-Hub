from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
from .serializers import CustomerSerializer, ProfileSerializer
from .models import Guest, Profile


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Only admins can manage customers

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

# Signal for creating profile on user creation

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
