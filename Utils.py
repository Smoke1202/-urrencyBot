import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: int):
        if quote.lower() == base.lower():
            raise ConvertionException(f'Конвертация одной и той же валюты это странно 🤯')
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f'Извините, но валюту {quote} мы не поддерживаем😔')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f'Извините, но валюту {base} мы не поддерживаем😔')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount} 😔')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[base_ticker] * amount
        total_base = round(total_base, 5)
        return total_base