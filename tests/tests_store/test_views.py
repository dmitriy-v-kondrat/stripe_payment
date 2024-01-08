import json

from store.views import stripe_config


def test_stripe_config(rf):
    response = stripe_config(rf.get('/config/'))
    assert response.status_code == 200
    keys = json.loads(response.content)
    assert 'publicKey' in keys.keys()
