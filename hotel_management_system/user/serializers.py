from rest_framework import serializers
from .models import Guest, Profile


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role']