import csv

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional


class AbstractCurrencyDataHandler(ABC):
    @abstractmethod
    def load_data(self) -> List[dict]:
        """Load data from the data source."""
        pass

    @abstractmethod
    def save_data(self, data: List[dict]):
        """Save data to the data source."""
        pass

    @abstractmethod
    def add_row(self, date: str, rates: dict):
        """Add a row to the data."""
        pass

    @abstractmethod
    def add_rows(self, data_to_add: List[dict]):
        """Add multiple rows to the data."""
        pass

    @abstractmethod
    def remove_old_rows(self, days: int):
        """Remove rows older than a specified number of days."""
        pass

    @abstractmethod
    def get_newest_date(self) -> Optional[str]:
        """Get the newest date from the data."""
        pass


class CurrencyDataHandlerCSV(AbstractCurrencyDataHandler):
    def __init__(self, filename: str):
        """
        Initialize the CurrencyDataHandlerCSV with a CSV file.

        Parameters:
        - filename (str): Name of the CSV file.
        """
        self.filename = filename

    def load_data(self, oldest_date: Optional[datetime] = None) -> List[dict]:
        """
        Load data from the CSV file.

        Returns:
        - List[dict]: List of dictionaries representing the loaded data.
        """
        data = []
        try:
            with open(self.filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if oldest_date and datetime.strptime(row['Date'], '%Y-%m-%d').date() < oldest_date.date():
                        continue

                    data.append(row)

        except FileNotFoundError:
            print(f"File '{self.filename}' not found. Creating a new data list.")

        return data

    def save_data(self, data: List[dict]):
        """
        Save data to the CSV file.

        Parameters:
        - data (List[dict]): List of dictionaries to be saved.
        """
        fieldnames = ['Date', 'EUR/PLN', 'USD/PLN', 'CHF/PLN', 'EUR/USD', 'CHF/USD']
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def add_row(self, date: str, rates: dict):
        """
        Add a row to the data.

        Parameters:
        - date (str): Date in the format '%Y-%m-%d'.
        - rates (dict): Dictionary containing currency rates.
        """
        def calculate_rate(dividend: float) -> float:
            """Calculate rates to USD."""
            return round(dividend / rates['USD'], 4)

        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format. Use '%Y-%m-%d'.")

        data = self.load_data()
        new_row = {
            'Date': date.strftime('%Y-%m-%d'),
            'EUR/PLN': rates['EUR'],
            'USD/PLN': rates['USD'],
            'CHF/PLN': rates['CHF'],
            'EUR/USD': calculate_rate(rates['EUR']),
            'CHF/USD': calculate_rate(rates['CHF']),
        }
        data.append(new_row)
        self.save_data(data)

    def add_rows(self, data_to_add: List[dict]):
        """
        Add multiple rows to the data.

        Parameters:
        - data_to_add (List[dict]): List of dictionaries containing date and currency rates.
        """
        for date, rates in data_to_add.items():
            self.add_row(date, rates)

    def remove_old_rows(self, days: int):
        """
        Remove rows older than a specified number of days.

        Parameters:
        - days (int): Number of days to keep.
        """
        oldest_date = datetime.now() - timedelta(days=days)
        data = self.load_data()
        data = [row for row in data if datetime.strptime(row['Date'], '%Y-%m-%d').date() >= oldest_date.date()]
        self.save_data(data)

    def get_newest_date(self) -> Optional[str]:
        """
        Get the newest date in the data.

        Returns:
        - str or None: The newest date in the format '%Y-%m-%d' or None if the data is empty.
        """
        data = self.load_data()
        if not data:
            return

        newest_date = max(row['Date'] for row in data)
        return newest_date
