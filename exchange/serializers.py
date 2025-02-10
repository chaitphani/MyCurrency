from rest_framework import serializers
from .models import CurrencyExchangeRate, Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ["valuation_date", "exchanged_currency", "rate_value"]
