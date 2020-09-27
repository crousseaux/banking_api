from rest_framework import serializers

from . import models


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Wallet


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Card


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Transfer
        depth = 2


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.User
