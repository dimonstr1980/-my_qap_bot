import json
import requests
from config import *


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Нельзя перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не смог обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не смог обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не смог обработать количество {amount}')

        r = requests.get(f'{site}price?fsym={quote_ticker}&tsyms={base_ticker}&api_key={api_key}')

        total_base = float(json.loads(r.content)[keys[base]]) * amount

        return total_base
