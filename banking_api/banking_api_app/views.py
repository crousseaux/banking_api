from rest_framework import generics

from .models import *
from .serializers import *


# Wallet views
class WalletList(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetail(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


# Transfer views
class TransferList(generics.ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class TransferDetail(generics.RetrieveAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


# Card views
class CardList(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDetail(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
