import requests
import random


class BaseExchangeAdapter:
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        raise NotImplementedError("This method should be implemented by child classes.")

class CurrencyBeaconAdapter(BaseExchangeAdapter):
    API_URL = "https://api.currencybeacon.com/v1/historical"
    API_KEY = "BGYOcEW9Xj7VpdfoJKGo2rcrzUInuPdU" # the key will be mentioned in ``.env` file to load from it secretly as an environment variable

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        params = {
            "api_key": self.API_KEY,
            "date": valuation_date.strftime("%Y-%m-%d"),
            "base": source_currency.code
        }
        response = requests.get(self.API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'].get(exchanged_currency.code)
            return rate if rate else None
        return None

class MockAdapter(BaseExchangeAdapter):
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        return round(random.uniform(0.5, 1.5), 6)
