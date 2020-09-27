from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Company)
admin.site.register(Currency)
admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Card)
admin.site.register(Transfer)
admin.site.register(Entity)