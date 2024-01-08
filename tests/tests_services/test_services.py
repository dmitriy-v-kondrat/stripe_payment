import pytest

from services.services import clean_session, discount_percentages


@pytest.mark.django_db
def test_clean_session(client):
    session = client.session
    session['order'] = '1'
    session['payment_intent'] = 'pi-1'
    session['session_id'] = 'id-1'
    assert 'order' in session.keys()
    assert 'payment_intent' in session.keys()
    assert 'session_id' in session.keys()
    clean_session(session)
    assert 'order' not in session.keys()
    assert 'payment_intent' not in session.keys()
    assert 'session_id' not in session.keys()


@pytest.mark.parametrize('price', [10, 30, 50, 70, 110])
def test_discount_percentages(price):
    discount = discount_percentages(price)

    if price == 10:
        assert discount is None
    if price == 30:
        assert discount == 5
    if price == 50:
        assert discount == 10
    if price == 70:
        assert discount == 15
    if price == 110:
        assert discount == 20
