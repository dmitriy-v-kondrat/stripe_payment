
from datetime import datetime

import requests
from django.conf import settings

RATE_API = settings.EXCHANGE_RATE_API
URL = f"https://v6.exchangerate-api.com/v6/{RATE_API}/pair/"
RATE_DICT = dict()


def get_exchange_data(order_currency: str, item_currency: str):
    response = requests.request("GET",
                                f"{URL}{order_currency}/{item_currency}"
                                )
    return response.json()


def get_exchange_rate(order_currency: str, item_currency: str) -> float:
    global RATE_DICT
    if not RATE_DICT or str(datetime.now()) > RATE_DICT.get('time'):
        response = get_exchange_data(order_currency, item_currency)
        time_update = datetime.strptime(response.get('time_next_update_utc'),
                                        '%a, %d %b %Y %H:%M:%S %z'
                                        )
        conversion_rate = response.get('conversion_rate')
        RATE_DICT.update(
                {'time': str(time_update),
                 'rate': conversion_rate
                 }
                )
    return RATE_DICT.get('rate')
