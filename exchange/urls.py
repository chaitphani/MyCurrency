from django.urls import path
from .views import CurrencyRatesListView, ConvertAmountView, CurrencyCRUDCreateView, CurrencyCRUDEditView


urlpatterns = [
    path("currency-rates/", CurrencyRatesListView.as_view(), name="currency_rates_list"),
    path("convert/", ConvertAmountView.as_view(), name="convert_amount"),
    path("currencies/", CurrencyCRUDCreateView.as_view(), name="currency_list_create"),
    path("currencies/<str:currency_code>/", CurrencyCRUDEditView.as_view(), name="currency_retrieve_update_delete")
]
