import pytest

from store.models import Item, Order
from tests.src.shemas.services_shemas.item_shema import ItemField

item_data = {'name': 'test',
             'description': 'test description',
             'price': '100',
             'currency': 'usd'}

item_data_2 = {'name': 'test 2',
               'description': 'test description 2',
               'price': '200',
               'currency': 'usd'}

item_data_3 = {'name': 'test 3',
               'description': 'test description 3',
               'price': '100',
               'currency': 'eur'}


@pytest.fixture
def item(db):
    ItemField(**item_data)
    items = Item.objects.create(**item_data)
    Item.objects.create(**item_data_2)
    Item.objects.create(**item_data_3)
    return items


@pytest.fixture
def order(db, item):
    order = Order.objects.create(total_price=item.price,
                                 pay_currency=item.currency
                                 )
    order.items.add(item, through_defaults={'item_ps': 1})
    return order
