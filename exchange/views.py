from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from .models import Currency, CurrencyExchangeRate
from .services import get_exchange_rate_data
from .serializers import ExchangeRateSerializer, CurrencySerializer


class CurrencyRatesListView(APIView):

    def get(self, request):
        source_currency_code = request.GET.get("source_currency")
        date_from_str = request.GET.get("date_from")
        date_to_str = request.GET.get("date_to")

        if not source_currency_code or not date_from_str or not date_to_str:
            return Response({"error": "Missing required parameters (source_currency, date_from, date_to)"}, status=400)

        try:
            date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format, expected YYYY-MM-DD"}, status=400)

        if date_from > date_to:
            return Response({"error": "date_from must be before or equal to date_to"}, status=400)

        source_currency = get_object_or_404(Currency, code=source_currency_code)

        exchange_rates = CurrencyExchangeRate.objects.filter(
            source_currency=source_currency,
            valuation_date__range=[date_from, date_to]
        ).order_by("valuation_date")

        if not exchange_rates.exists():
            return Response({"error": "No exchange rates found for the given criteria"}, status=404)

        serializer = ExchangeRateSerializer(exchange_rates, many=True)
        return Response(serializer.data)


class ConvertAmountView(APIView):

    def get(self, request):
        source_currency = get_object_or_404(Currency, code=request.GET.get("source_currency"))

        try:
            amount = float(request.GET.get("amount", 1))
            if amount <= 0:
                return Response({"error": "Amount must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

        exchanged_currency = request.GET.get("exchanged_currency", None)
        valuation_date = date.today()
        available_currencies = Currency.objects.exclude(code=source_currency.code)

        conversion_results = {}
        for currency in available_currencies:
            rate = get_exchange_rate_data(source_currency, currency, valuation_date)
            if rate:
                converted_amount = round(amount * float(rate), 2)
                conversion_results[currency.code] = {
                    "rate": rate,
                    "converted_amount": converted_amount
                }

        if exchanged_currency:
            if exchanged_currency in conversion_results:
                return Response({
                    "source_currency": source_currency.code,
                    "amount": amount,
                    "exchanged_currency": exchanged_currency,
                    "rate": conversion_results[exchanged_currency]["rate"],
                    "converted_amount": conversion_results[exchanged_currency]["converted_amount"]
                })
            else:
                return Response({"error": f"No exchange rate found for {exchanged_currency}"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "source_currency": source_currency.code,
            "amount": amount,
            "conversion_results": conversion_results
        })


class CurrencyCRUDCreateView(APIView):

    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrencyCRUDEditView(APIView):

    def get(self, request, currency_code):
        currency = Currency.objects.filter(code=currency_code)
        if len(currency) > 0:
            serializer = CurrencySerializer(currency.last())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Currency not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, currency_code):
        currency = Currency.objects.filter(code=currency_code)
        if len(currency) > 0:
            serializer = CurrencySerializer(currency.last(), data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, currency_code):
        currency = Currency.objects.filter(code=currency_code)
        if len(currency) > 0:
            currency.last().delete()
            return Response({"message": "Currency deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Currency not found"}, status=status.HTTP_400_BAD_REQUEST)
