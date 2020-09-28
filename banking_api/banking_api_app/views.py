import decimal

from rest_framework import generics, status
from rest_framework.response import Response

from banking_api.banking_api_app.services import permission_service, transfer_service
from .models import *
from .serializers import *


# Wallet views
class WalletList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def create(self, request, *args, **kwargs):
        company_id = int(request.headers.get('Company-Id'))
        if not permission_service.is_employee(request, company_id):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        wallet = Wallet.objects.create(**request.data)
        Entity.objects.create(wallet=wallet)
        return Response(WalletSerializer(wallet).data, status=status.HTTP_201_CREATED)


class WalletDetail(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


# Transfer views
class TransferList(generics.ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        amount = data.get('amount')
        if amount is None or amount < 0:
            return Response({'error': 'Please provide a positive decimal as the amount'}, status=status.HTTP_400_BAD_REQUEST)
        origin_entity_id = data.get('origin_entity_id')
        target_entity_id = data.get('target_entity_id')
        company_id = int(request.headers.get('Company-Id'))
        user_id = int(request.headers.get('User-Id'))
        if not permission_service.is_employee(request, company_id) and not permission_service.is_user(request, user_id):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        amount = decimal.Decimal(amount)
        return transfer_service.execute_transfer(amount, origin_entity_id, target_entity_id)


class TransferDetail(generics.RetrieveAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


# Card views
class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def create(self, request, *args, **kwargs):
        user_id = int(request.headers.get('User-Id'))
        if not permission_service.is_user(request, user_id):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        card = Card.objects.create(**request.data)
        Entity.objects.create(card=card)
        return Response(CardSerializer(card).data, status=status.HTTP_201_CREATED)


class CardDetail(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


# User views
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCards(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        user_pk = self.kwargs['pk']
        return self.queryset.filter(user=user_pk)


class UserWallets(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        user_pk = self.kwargs['pk']
        user_cards = Card.objects.filter(user=user_pk)
        user_wallets = {}
        for user_card in user_cards:
            if user_wallets.get(user_card.wallet.id) is None:
                user_wallets[user_card.wallet.id] = user_card.wallet
        return user_wallets.values()
