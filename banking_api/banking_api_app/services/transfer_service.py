import decimal

import requests
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.response import Response

from banking_api.banking_api_app import models
from banking_api.banking_api_app.models import Card
from banking_api.banking_api_app.serializers import TransferSerializer

CONVERSION_FEE = decimal.Decimal(0.029)


def execute_transfer(amount, origin_entity_id, target_entity_id):
    origin_entity = models.Entity.objects.get(id=origin_entity_id)
    if origin_entity is None:
        return Response({'error': 'Origin entity is missing or incorrect. Make sure to provide a correct origin entity'}, status=status.HTTP_400_BAD_REQUEST)

    target_entity = models.Entity.objects.get(id=target_entity_id)
    if target_entity is None:
        return Response({'error': 'Target entity is missing or incorrect. Make sure to provide a correct target entity'}, status=status.HTTP_400_BAD_REQUEST)

    if origin_entity.get_balance() < amount:
        return Response({'error': 'Not enough money in entity'}, status=status.HTTP_400_BAD_REQUEST)

    fees = 0
    # if currencies are different, we apply fees depending on converison rate
    if origin_entity.get_currency().id != target_entity.get_currency().id:
        try:
            # call to api to retrieve latest exchange rates
            conversion_rate = get_currency_conversion(origin_entity.get_currency(), target_entity.get_currency())
        except HTTPError:
            return Response({'error': 'Unable to get connect to foreign exchange rates API. Please try again.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if conversion_rate is None:
            return Response({'error': 'Currency not recognized by API, make sure currency code is correct'})
        # target amount after conversion
        target_amount = amount * decimal.Decimal(conversion_rate)
        # calculate fees
        fees = target_amount * CONVERSION_FEE
        # target amount after removing fees
        target_amount -= fees
        # remove original amount from origin entity
        origin_entity.set_balance(origin_entity.get_balance() - amount)
        # add amount after conversion and subtracting fees to target entity
        target_entity.set_balance(target_entity.get_balance() + target_amount)
        # add amount to correct master wallet
        master_wallet = get_master_wallet_for_currency(target_entity.get_currency().id)
        master_wallet.balance += fees
        master_wallet.save()
    else:
        # in case entities are in same currency, there is no fees
        origin_entity.set_balance(origin_entity.get_balance() - amount)
        target_entity.set_balance(target_entity.get_balance() + amount)

    transfer = models.Transfer.objects.create(origin_entity=origin_entity, origin_currency=origin_entity.get_currency(), target_entity=target_entity,
                                              target_currency=target_entity.get_currency(), amount=amount, conversion_fee=fees)
    return Response(TransferSerializer(transfer).data, status=status.HTTP_201_CREATED)


# helper function to retrieve conversion rates from a given base currency to a target currency using exchange rates api
def get_currency_conversion(origin_currency, target_currency):
    resp = requests.get('https://api.exchangeratesapi.io/latest', params={'base': origin_currency.code, 'symbols': target_currency.code})
    resp.raise_for_status()
    resp = resp.json()
    conversion_rate = resp["rates"][target_currency.code] if resp["rates"] and resp["rates"][target_currency.code] else None
    return conversion_rate


def get_master_wallet_for_currency(currency_id):
    return models.Wallet.objects.get(is_master=True, currency=currency_id)


def get_card(card_id):
    return Card.objects.get(id=card_id)


# block card: unload money into wallet and creates a transfer record
def block_card(card_id):
    card = get_card(card_id)
    amount = card.balance
    origin_entity = models.Entity.objects.get(card=card)
    target_entity = models.Entity.objects.get(wallet=card.wallet)
    execute_transfer(amount, origin_entity.id, target_entity.id)
    card = get_card(card_id)
    card.status = "Blocked"
    card.save()


# unblock card: re-activate the card
def unblock_card(card_id):
    card = get_card(card_id)
    card.status = "Active"
    card.save()
