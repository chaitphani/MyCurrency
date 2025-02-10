from django.contrib import admin
from .models import CurrencyExchangeRate, Currency, Provider


admin.site.register(CurrencyExchangeRate)
admin.site.register(Currency)
admin.site.register(Provider)
