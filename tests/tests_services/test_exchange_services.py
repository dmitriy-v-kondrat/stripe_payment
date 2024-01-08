import json

import pytest

from services.exchange_services import get_exchange_data, get_exchange_rate
from tests.src.shemas.services_shemas.exchange_shema import Exchange

exchange_data = {
    'result': 'success',
    'documentation': 'https://www.exchangerate-api.com/docs',
    'terms_of_use': 'https://www.exchangerate-api.com/terms',
    'time_last_update_unix': 1702425601,
    'time_last_update_utc': 'Wed, 13 Dec 2023 00:00:01 +0000',
    'time_next_update_unix': 1702512001,
    'time_next_update_utc': 'Thu, 14 Dec 2023 00:00:01 +0000',
    'base_code': 'EUR',
    'target_code': 'USD',
    'conversion_rate': 3
    }


@pytest.mark.skip(reason='Paid access to currency converter.')
@pytest.mark.parametrize('base_code, target_code', [('eur', 'usd'),
                                                    ('usd', 'eur'),
                                                    ]
                         )
def test_get_exchange_data(base_code, target_code):
    response = get_exchange_data(base_code, target_code)
    assert response.get('result') == 'success'
    assert Exchange.model_validate_json(json.dumps(response))


@pytest.mark.parametrize('base_code, target_code', [('eur', 'usd'),
                                                    ('usd', 'eur'),
                                                    ]
                         )
def test_get_exchange_rate(monkeypatch, base_code, target_code):
    def mock_get_exchange_data(*args, **kwargs):
        return exchange_data

    monkeypatch.setattr('services.exchange_services.get_exchange_data',
                        mock_get_exchange_data
                        )

    result = get_exchange_rate(base_code, target_code)
    assert result == 3
