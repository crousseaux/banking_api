from django.core.management.base import BaseCommand

from banking_api.banking_api_app.models import *


class Command(BaseCommand):
    help = 'Populates database with companies, users, currencies, wallets, cards'

    def handle(self, *args, **options):
        # delete any existing data
        Card.objects.all().delete()
        print('Cards deleted')
        Wallet.objects.all().delete()
        print('Wallets deleted')
        Currency.objects.all().delete()
        print('Currency deleted')
        User.objects.all().delete()
        print('Users deleted')
        Company.objects.all().delete()
        print('Company deleted')
        # create new data
        create_companies()
        print('Companies created')
        create_users()
        print('Users created')
        create_currencies()
        print('Currencies created')
        create_wallets()
        print('Wallets created')
        create_cards()
        print('Cards created')
        create_entities()


def create_companies():
    company_list = ['Spendesk', 'Salesforce', 'My Company']
    companies = []
    for company_name in company_list:
        new_company = Company(name=company_name)
        companies.append(new_company)
    Company.objects.bulk_create(companies)


def create_users():
    user_list = [{'name': 'Anna M', 'company': 'Salesforce'}, {'name': 'Marie A', 'company': 'Salesforce'}, {'name': 'Peter D', 'company': 'My Company'}]
    users = []
    for user in user_list:
        first_name, last_name = user.get('name').split(' ')
        print(user.get('company'))
        company = Company.objects.get(name=user.get('company'))
        print(company)
        new_user = User(first_name=first_name, last_name=last_name, company=company)
        users.append(new_user)
    User.objects.bulk_create(users)


def create_currencies():
    currency_list = {'EUR': '€', 'USD': '$', 'GBP': '£'}
    currencies = []
    for code, symbol in currency_list.items():
        new_currency = Currency(code=code, symbol=symbol)
        currencies.append(new_currency)
    Currency.objects.bulk_create(currencies)


def create_wallets():
    wallet_list = [{'company': 'Spendesk', 'balance': 0, 'currency': 'EUR', 'is_master': True},
                   {'company': 'Spendesk', 'balance': 0, 'currency': 'USD', 'is_master': True},
                   {'company': 'Spendesk', 'balance': 0, 'currency': 'GBP', 'is_master': True},
                   {'company': 'Salesforce', 'balance': 100, 'currency': 'EUR', 'is_master': False},
                   {'company': 'Salesforce', 'balance': 100, 'currency': 'USD', 'is_master': False},
                   {'company': 'My Company', 'balance': 100, 'currency': 'GBP', 'is_master': False}]
    wallets = []
    for wallet in wallet_list:
        company = Company.objects.get(name=wallet.get('company'))
        currency = Currency.objects.get(code=wallet.get('currency'))
        new_wallet = Wallet(company=company, currency=currency, balance=wallet.get('balance'), is_master=wallet.get('is_master'))
        wallets.append(new_wallet)
    Wallet.objects.bulk_create(wallets)


def create_cards():
    card_list = [{'company': 'Salesforce', 'balance': 10, 'currency': 'EUR', 'number': 1111111111111111,
                  'expiration_date': '2020-10-28', 'ccv': 111, 'user': 'Anna M'},
                 {'company': 'Salesforce', 'balance': 10, 'currency': 'USD', 'number': 2222222222222222,
                  'expiration_date': '2020-10-28', 'ccv': 222, 'user': 'Anna M'},
                 {'company': 'Salesforce', 'balance': 10, 'currency': 'EUR', 'number': 3333333333333333,
                  'expiration_date': '2020-10-28', 'ccv': 333, 'user': 'Marie A'},
                 {'company': 'My Company', 'balance': 10, 'currency': 'GBP', 'number': 4444444444444444,
                  'expiration_date': '2020-10-28', 'ccv': 444, 'user': 'Peter D'},
                 ]
    cards = []
    for card in card_list:
        company = Company.objects.get(name=card.get('company'))
        currency = Currency.objects.get(code=card.get('currency'))
        first_name, last_name = card.get('user').split(' ')
        user = User.objects.get(first_name=first_name, last_name=last_name)
        wallet = Wallet.objects.get(company=company, currency=currency)
        # by default status will be active
        new_card = Card(wallet=wallet, balance=card.get('balance'), currency=currency, number=card.get('number'),
                        expiration_date=card.get('expiration_date'), ccv=card.get('ccv'), user=user)
        cards.append(new_card)
    Card.objects.bulk_create(cards)


def create_entities():
    entities = []
    cards = Card.objects.all()
    wallets = Wallet.objects.all()
    for card in cards:
        entity = Entity(card=card)
        entities.append(entity)
    for wallet in wallets:
        entity = Entity(wallet=wallet)
        entities.append(entity)
    Entity.objects.bulk_create(entities)
