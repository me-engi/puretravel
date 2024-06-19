from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Customer, ShopOwner, Tourguide


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'phone_number', 'address']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance


class TourguideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourguide
        fields = ['username', 'email', 'password', 'phone_number', 'address']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance


class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = ['username', 'email', 'password', 'phone_number', 'address']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance
