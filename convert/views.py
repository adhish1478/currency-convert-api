from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# Create your views here.
class CurrencyConverterView(APIView):
    def post(self, request):
        amount= request.data.get('amount')
        from_currency= request.data.get('from_currency')
        to_currency= request.data.get('to_currency')

        if not amount or not from_currency or not to_currency:
            return Response({'error': 'Amount, from_currency, and to_currency are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # External API URL to get exchange rates
        api_key= 'ab69391e71becf6e0438c11f'
        url=  f"https://v6.exchangerate-api.com/v6/ab69391e71becf6e0438c11f/latest/{from_currency}"
        response= requests.get(url)
        data= response.json()

        if 'conversion_rates' not in data:
            return Response({"error": "Failed to get exchange rates."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        exchange_rate= data['conversion_rates'].get(to_currency)
        if not exchange_rate:
            return Response({'error': 'Invalid target currency code'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Convert the amount
        converted_amount= amount * exchange_rate
        return Response({
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'converted_amount': converted_amount,
            'exchange_rate': exchange_rate
        }, status=status.HTTP_200_OK)