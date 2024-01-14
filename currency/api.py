
from typing import Dict, List, Optional

from django.http import HttpResponseForbidden, JsonResponse
from ninja import NinjaAPI

from currency.handlers import CurrencyDataHandlerCSV


api = NinjaAPI()
import logging
logger = logging.getLogger(__name__)

@api.get("/rates")
def get_currency_rates(request, currencies: Optional[List[str]] = None):
    """
    Get the currency rates for the specified currency pair(s).

    :param request: Django request object
    :param currencies: Either a single currency pair (e.g., "USD/PLN") or a list of currency pairs.
                       Example: "USD/PLN" or ["USD/PLN", "EUR/PLN"]
    :return: JsonResponse list rates for the specified currency pair(s)
    """
    # Parse the currency pairs from the query parameter
    currencies = currencies.split(',') if currencies else []

    handler = CurrencyDataHandlerCSV("all_currency_data.csv")
    currencies_data = handler.load_data()

    if not currencies_data:
        return JsonResponse({"data": {}})
    if not currencies:
        currencies = list(currencies_data[0].keys())
        currencies.remove('Date')

    for currency in currencies:
        if currency not in currencies_data[0]:
            return HttpResponseForbidden(f"Invalid currency specified ({currency}). Access denied.")

    return JsonResponse({"data": get_formatted_data(currencies, currencies_data)})


def get_formatted_data(currencies: List[str], currencies_data: List[Dict[str, str]]) -> Dict[str, dict]:
    data = {}
    for currency in currencies:
        rates = []
        formatted_rates = []
        for row in currencies_data:
            value = float(row[currency])
            rates.append(value)
            formatted_rates.append({row['Date']: value})

        no_rates = len(rates)

        data[currency] = {
            'avg': sum(rates) / no_rates,
            'median': sorted(rates)[no_rates // 2],
            'min': min(rates),
            'max': max(rates),
            'count': no_rates,
            'rates': formatted_rates,
        }

    return data
