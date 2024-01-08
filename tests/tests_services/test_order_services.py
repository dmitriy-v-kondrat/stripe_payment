import pytest

from services.order_services import order_formation


def test_create_order(client, item):
    """
    If not session.get('order').
    Create Order and save it to session.
    """
    # OrderField(total_price=item.price, pay_currency=item.currency, items=item)
    session = client.session
    assert not session.get('order')
    order = order_formation(session, pk=1)
    assert session.get('order')
    assert session.get('order') == str(order.id)
    assert order.orderitem_set.values()[0].get('item_ps') == 1


@pytest.mark.django_db
@pytest.mark.parametrize('item_ids', [1, 2])
def test_order_formation_currency_equal(client, order, item_ids):
    """
    If session.get('order').
    Get Order and Item instances.
    If order currency equal item currency.
    """

    item_ps = order.orderitem_set.values()[0].get('item_ps')
    session = client.session
    session['order'] = str(order.id)
    session.save()
    order = order_formation(session, pk=item_ids)
    order_price = order.total_price

    if item_ids == 1:
        assert order_price == 200
        assert order.items.count() == order.orderitem_set.count() == 1
        assert order.orderitem_set.values()[0].get(
                'item_ps') == item_ps + 1
    if item_ids == 2:
        assert order_price == 300
        assert order.items.count() == order.orderitem_set.count() == 2
        assert order.orderitem_set.values()[0].get('item_ps') == item_ps


@pytest.mark.django_db
@pytest.mark.parametrize('item_ids', [3])
def test_order_formation_currency_not_equal(client,
                                            monkeypatch,
                                            order,
                                            item_ids
                                            ):
    """
    If session.get('order').
    Get Order and Item instances.
    If order currency not equal item currency.
    """

    item_ps = order.orderitem_set.values()[0].get('item_ps')
    session = client.session
    session['order'] = str(order.id)
    session.save()

    def mock_get_exchange_rate(*args, **kwargs):
        return 2.00

    monkeypatch.setattr('services.order_services.get_exchange_rate',
                        mock_get_exchange_rate
                        )

    order = order_formation(session, pk=item_ids)
    order_price = order.total_price

    assert order_price == 150
    assert order.items.count() == order.orderitem_set.count() == 2
    assert order.orderitem_set.values()[0].get('item_ps') == item_ps


def test_items_ordered():
    ...
