from django.urls import path
from .views import CurrencyConverterView

urlpatterns=[
    path('converter/', CurrencyConverterView.as_view(), name='currency_converter'),
]