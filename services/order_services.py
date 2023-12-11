
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from services.exchange_services import get_exchange_rate
from store.models import Item, Order


def order_formation(session, **kwargs):
    """
     Create or update order instance.
     Add item, convert price item currency to order currency
     and update total price.
    """
    if session.get('order'):
        try:
            order = Order.objects.get(id=session.get('order'), payment=False)
            item = Item.objects.get(pk=kwargs['pk'])
            if order.pay_currency == item.currency:
                order.total_price += item.price
            else:
                item_currency = item.get_currency_display()
                order_currency = order.get_pay_currency_display()
                conversion_rate = get_exchange_rate(order_currency=
                                                    order_currency,
                                                    item_currency=
                                                    item_currency
                                                    )
                price = item.price // conversion_rate
                order.total_price += price
            order.save()
            order_items, b = order.orderitem_set.get_or_create(order_id=
                                                               order.id,
                                                               item_id=
                                                               item.id,
                                                               )
            order_items.item_ps = F('item_ps') + 1
            order_items.save()
            return order

        except ObjectDoesNotExist:
            return 'This order is paid. Call administrator'

    else:
        order = create_order(**kwargs)
        session['order'] = str(order.id)
        session.save()
        return order


def create_order(**kwargs):
    """ Create order. """
    item = Item.objects.get(pk=kwargs['pk'])
    order = Order.objects.create(total_price=item.price,
                                 pay_currency=item.currency
                                 )
    order.items.add(item.id, through_defaults={'item_ps': 1})

    return order


def items_ordered(item):
    """ Create a dictionary. """
    items_str = str()
    for i in item:
        items_str += f" id: {i.get('item_id')}," \
                     f" name: {i.get('item__name')}," \
                     f" count: {i.get('item_ps')};\n "
    return items_str
