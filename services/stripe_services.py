import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET
STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY

RETURN_URL = 'http://127.0.0.1:8000/'


def public_key():
    """ Return stpipe public key. """
    return {'publicKey': settings.STRIPE_PUBLIC_KEY}


def create_tax_calculation(order, address):
    """ Create stripe tax calculation. """
    calculation = stripe.tax.Calculation.create(
            currency=order.get_pay_currency_display(),
            line_items=[{"amount": order.total_price, "reference": order.id}],
            customer_details={
                'address': {
                    'line1': address.get('line1', ''),
                    'line2': address.get('line2', ''),
                    'city': address.get('city', ''),
                    'state': address.get('state', ''),
                    'postal_code': address.get('postal_code', ''),
                    'country': address.get('country', ''),
                    },
                'address_source': 'billing'
                },
            expand=['line_items.data.tax_breakdown']
            )
    return calculation


def create_customer(address):
    """ Create stripe customer. """
    customer = stripe.Customer.create(email=address.pop('email', ''),
                                      address={**address},
                                      expand=["tax"]
                                      )
    return customer


def create_payment_intent(calculation,
                          order,
                          customer_id
                          ):
    """ Create stripe payment intent. """
    payment_intent = stripe.PaymentIntent.create(
            amount=calculation.amount_total * 100,
            currency=order.get_pay_currency_display(),
            metadata={"tax_calculation": calculation.id},
            description=order.id,
            automatic_payment_methods={"enabled": True},
            customer=customer_id,
            )
    return payment_intent


def retrieve_payment_intent(payment_session):
    """ Retrieve stripe payment intent. """
    payment_intent = stripe.PaymentIntent.retrieve(payment_session)
    return payment_intent


def retrieve_tax(tax_calculation):
    """ Retrieve stripe tax calculation. """
    payment_tax = stripe.tax.Calculation.list_line_items(tax_calculation)
    return payment_tax


def create_coupon(percent: int):
    """ Create stripe coupon. """
    if percent:
        coupon = stripe.Coupon.create(percent_off=percent, duration="once")
        return coupon


def create_tax_rate(tax: int):
    """ Create stripe tax rate. """
    tax_rate = stripe.TaxRate.create(
            display_name="Sales Tax",
            inclusive=False,
            percentage=tax,
            )
    return tax_rate


def dict_discount(discount):
    """ Returns coupon if there is a discount. """
    if discount:
        return [{"coupon": create_coupon(discount).id}]


def create_stripe_session(order, items_str, tax, discount):
    """ Create stripe session. """
    checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    'price_data': {
                        'currency': order.get_pay_currency_display(),
                        'unit_amount': order.total_price * 100,
                        'product_data': {
                            'name': 'Items',
                            'description': items_str,
                            'images': [],
                            },

                        },
                    "tax_rates": [create_tax_rate(tax).id],
                    'quantity': 1,
                    }],
            discounts=dict_discount(discount),
            mode='payment',
            success_url=f"{RETURN_URL}success/",
            cancel_url=f"{RETURN_URL}cancel.html",
            )
    return checkout_session


def retrieve_stripe_session(session_id):
    """ Retrieve stripe session. """
    return stripe.checkout.Session.retrieve(session_id)
