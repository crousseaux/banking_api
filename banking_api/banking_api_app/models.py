from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
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


class Transfer(BaseModel):
    amount = models.IntegerField()
    origin_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='origin_transfers')
    target_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='target_transfers')
    conversion_fee = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    # generic relation for the origin entity
    origin_entity_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='origin_transfers')
    origin_entity_id = models.PositiveIntegerField()
    origin_entity_object = GenericForeignKey('origin_entity_type', 'origin_entity_id')
    # generic relation for the target entity
    target_entity_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='target_transfers')
    target_entity_id = models.PositiveIntegerField()
    target_entity_object = GenericForeignKey('target_entity_type', 'target_entity_id')


class Wallet(BaseModel):
    balance = models.IntegerField(unique=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    is_master = models.BooleanField(default=False)
    transfer = GenericRelation(Transfer)


class Card(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    number = models.IntegerField()
    # todo: (creation + 1 month) ?
    expiration_date = models.DateTimeField()
    ccv = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(choices=(('Active', 'Active'), ('Blocked', 'Blocked')), default='Active', max_length=10)
    transfer = GenericRelation(Transfer)
