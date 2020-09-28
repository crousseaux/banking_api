from datetime import timedelta, date
from random import randint

from django.db import models


# Abstract base model: holds common base fields which will be added to child models
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# currencies supported
class Currency(BaseModel):
    code = models.CharField(max_length=5)
    symbol = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = "Currencies"


class Company(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Companies"


class User(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)


class Wallet(BaseModel):
    balance = models.DecimalField(default=100, decimal_places=2, max_digits=15)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    is_master = models.BooleanField(default=False)


class Card(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    balance = models.DecimalField(default=10, decimal_places=2, max_digits=15)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    number = models.IntegerField(default=100)
    expiration_date = models.DateField(null=True, blank=True)
    ccv = models.IntegerField(default=1000000000000000)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(choices=(('Active', 'Active'), ('Blocked', 'Blocked')), default='Active', max_length=10)

    def create(self, *args, **kwargs):
        self.expiration_date = date.today() + timedelta(days=30)
        self.ccv = randint(100, 999)
        self.number = randint(1000000000000000, 9999999999999999)
        super(Card, self).save(*args, **kwargs)


class Entity(BaseModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True, related_name='entity')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True, null=True, related_name='entity')

    class Meta:
        verbose_name_plural = "Entities"

    def get_currency(self):
        if self.card is not None:
            return self.card.currency
        else:
            return self.wallet.currency

    def get_balance(self):
        if self.card is not None:
            return self.card.balance
        else:
            return self.wallet.balance

    def set_balance(self, new_balance):
        if self.card is not None:
            self.card.balance = new_balance
            self.card.save()
        else:
            self.wallet.balance = new_balance
            self.wallet.save()


class Transfer(BaseModel):
    amount = models.IntegerField()
    origin_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='origin_transfers')
    target_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='target_transfers')
    conversion_fee = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    origin_entity = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name='origin_transfers')
    target_entity = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name='target_transfers')
