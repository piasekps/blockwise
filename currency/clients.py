import requests

from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union


class AbstractAPIClient(ABC):
    """
    Abstract base class for NBP API clients.
    """

    @abstractmethod
    def get_exchange_rates(
        self, currencies: Tuple[str], days: Optional[int] = 0, start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None, base_currency: Optional[str] = None,
    ) -> Union[Dict[str, Dict[str, float]], Dict[str, str]]:
        """
        Retrieve exchange rates for specified currencies against the base currency for the last specified number of days.

        Parameters:
        - currencies (Tuple[str]): List of currencies to retrieve exchange rates for.
        - days (Optional[int]): Number of days to retrieve exchange rates for.
        - start_date (Optional[datetime]): Start date to retrieve rates for.
        - end_date (Optional[datetime]): End date to retrieve rates for.
        - base_currency (Optional[str]): Base currency code.

        """
        pass


class NBPAPIClient(AbstractAPIClient):
    """
    A simple client to retrieve exchange rates from the NBP API.

    Usage:
    client = NBPAPIClient()
    data = client.get_exchange_rates(["EUR", "USD", "CHF"], 90)
    """
    base_url = 'http://api.nbp.pl/api/exchangerates/rates/A'

    def get_exchange_rates(
        self, currencies: Tuple[str], days: Optional[int] = 0, start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = datetime.now(), base_currency: Optional[str] = None,
    ) -> Union[Dict[str, Dict[str, float]], Dict[str, str]]:
        """
        Retrieve exchange rates for specified currencies against the base currency for the last specified number of days.

        Parameters:
        - currencies (Tuple[str]): List of currencies to retrieve exchange rates for.
        - days (Optional[int]): Number of days to retrieve exchange rates for.
        - start_date (Optional[datetime]): Start date to retrieve rates for.
        - end_date (Optional[datetime]): End date to retrieve rates for.
        - base_currency (Optional[str]): Base currency code. Not used, default PLN!

        Returns:
        - Union[Dict[str, List[Dict[str, Union[str, float]]]], Dict[str, str]]: Exchange rates data or error message.
        """
        if days:
            start_date = end_date - timedelta(days=days)

        if not (start_date or days):
            raise Exception('Provide either days or date range.')

        exchange_rates_data = defaultdict(dict)

        for currency in currencies:
            response = requests.get(f"{self.base_url}/{currency}/{start_date:%Y-%m-%d}/{end_date:%Y-%m-%d}/")

            if response.status_code != 200:
                return {"error": f"Failed to fetch data for {currency}"}

            data = response.json()
            for entry in data['rates']:
                exchange_rates_data[entry['effectiveDate']][currency] = entry['mid']

        return exchange_rates_data
