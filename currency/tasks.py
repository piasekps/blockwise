from celery import shared_task

from currency.clients import NBPAPIClient
from currency.handlers import CurrencyDataHandlerCSV


@shared_task
def fetch_currency_data_task():
    """
    Task to fetch currency exchange rates, update the database, and remove old data.

    This task fetches exchange rates for specified currencies from a provider, updates the database,
    and removes rows older than a specified number of days.

    :param None
    :return: None
    """
    days_to_keep = 90
    currencies = ["USD", "EUR", "CHF"]
    handler = CurrencyDataHandlerCSV("all_currency_data.csv")
    client = NBPAPIClient()
    # update DB and remove old data
    handler.remove_old_rows(days_to_keep)

    # retrieve data from provider
    data = client.get_exchange_rates(currencies, days_to_keep)
    handler.add_rows(data)
