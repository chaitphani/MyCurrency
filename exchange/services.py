from .models import CurrencyExchangeRate, Provider
from .adapters import CurrencyBeaconAdapter, MockAdapter


def provider_service(provider, source_currency, exchanged_currency, valuation_date):

    adapter = CurrencyBeaconAdapter() if provider.name == "CurrencyBeacon" else MockAdapter()
    rate_value = adapter.get_exchange_rate(source_currency, exchanged_currency, valuation_date)
    if rate_value:
        CurrencyExchangeRate.objects.create(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=valuation_date,
            rate_value=rate_value
        )
        return rate_value

            
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider=None):

    provider_service = provider_service(provider, source_currency, exchanged_currency, valuation_date)

    rate = CurrencyExchangeRate.objects.filter(
        source_currency=source_currency,
        exchanged_currency=exchanged_currency,
        valuation_date=valuation_date
    ).first()

    if rate:
        return rate.rate_value

    if provider:
        provider_service

    providers = Provider.objects.filter(is_active=True).order_by("priority")
    for provider in providers:
        provider_service

    return None
