from datetime import datetime
from enum import Enum
from pprint import pprint
from typing import Optional, List

import requests


class WhUnits(Enum):
    KILO = 'Kilo'
    MEGA = 'Mega'


class PriceUnits(Enum):
    EUR = 'Eur'
    EUR_CENTS = 'EUR Cents'


class NordPoolPrice:
    URL = 'https://nordpoolprice.codeborne.com/api/prices?country={}'

    @staticmethod
    def get_prices(
            country: str,
            wh_units: WhUnits = WhUnits.KILO,
            price_units: PriceUnits = PriceUnits.EUR_CENTS,
            vat_percentage: Optional[float] = None,
            date: Optional[datetime] = None
    ) -> List[float]:
        """
        Get prices from NordPool.

        :param country: Country for which to get prices.
        :param wh_units: Choose for which unit to measure the price. For example, MWh, kWh, etc.
        :param price_units: Choose in which currency units to represent the price. For example, Eur, Eur cents, etc.
        :param vat_percentage: If you want prices to be calculated with VAT, provide one here. For example, 20.
        :param date: Date for which to get prices. If not provided - defaults to today.

        :return: List of prices. List always contains 24 items representing 24 hours. For example, a first item
            within a list represents a price between 00:00 and 01:00, the second item represents between
            01:00 and 02:00, and so on.
        """
        now = datetime.now().date()

        # Retrieve prices from official NordPool API.
        response = requests.get(NordPoolPrice.URL.format(country))

        if response.status_code != 200:
            raise Exception(
                f'Received non-200 HTTP status code from NordPool API. '
                f'Consider checking if given country name is correct. '
                f'Full response:\n{response.content}.'
            )

        # The response from NordPool API is always JSON, unless we don't get HTTP 200.
        response = response.json()

        try:
            # The JSON contains string dates (e.g. '2024-01-17') as keys and a list of prices as values.
            # Prices are represented as float numbers. The list will always contain 24 prices representing 24 hours.
            prices = response[str(date.date() if date else now)]
        except KeyError as ex:
            available_keys_formatted = ', '.join(response.keys())
            raise KeyError(f'No price for {ex} date. Available dates (keys) are: {available_keys_formatted}.')

        if len(prices) != 24:
            raise ValueError(
                f'Got a response from NordPool API that does not contain 24 items. '
                f'This is unexpected. Got {len(prices)} items. Full response given below:\n{pprint(response)}.'
            )

        # Convert units. By default, the API returns units in MWh.
        if wh_units == WhUnits.KILO:
            prices = [p / 1000 for p in prices]

        # Convert price. By default, the API returns prices in EUR.
        if price_units == PriceUnits.EUR_CENTS:
            prices = [p * 100 for p in prices]

        # Adjust for VAT. By default, the API does not include VAT.
        if vat_percentage is not None:
            prices = [p + p * (vat_percentage / 100) for p in prices]

        # Round prices with 2 precision points.
        prices = [round(p, 2) for p in prices]

        return prices
