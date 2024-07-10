import json
import requests
from config import keys


class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            iso_quote = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            iso_base = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ConvertionException(f'Не удалость обработать количество {amount}')

        except ValueError:
            raise ConvertionException(f'Не удалость обработать количество {amount}')

        if base == quote:
            raise ConvertionException('Нельзя конвертировать в точно такую же валюту')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={iso_quote}&tsyms={iso_base}').content
        converted = json.loads(r)

        total = float(amount) * converted[iso_base]

        return round(total, 3)
