import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from services.order_services import items_ordered, order_formation
from services.services import clean_session, discount_percentages
from store.models import Discount, Item, Order, Tax
from services.stripe_services import (create_customer,
                                      create_payment_intent,
                                      create_tax_calculation,
                                      public_key,
                                      retrieve_payment_intent,
                                      retrieve_stripe_session,
                                      retrieve_tax,
                                      create_stripe_session
                                      )

STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET


def stripe_config(request):
    if request.method == 'GET':
        return JsonResponse(public_key(), safe=False)


class ItemListView(ListView):
    """ List all items. """
    model = Item
    template_name = 'item-list.html'


class ItemDetailView(DetailView):
    """ Detail choice item. """
    model = Item
    template_name = 'item.html'


class OrderCreateView(View):
    """ Create or update order. """

    def get(self, request, *args, **kwargs):
        try:
            order = order_formation(request.session, **kwargs)
            return redirect('order', order)

        except Exception:
            messages.error(request, 'This order is paid. Call administrator')
            return redirect('error')


class OrderDetailView(DetailView):
    """ Detail order. """
    model = Order
    template_name = 'order.html'


class CheckoutView(View):
    """
    Create stripe session for payment now,
    with tax rate and discount.
    """

    def get(self, request, **kwargs):
        order = Order.objects.get(id=request.session.get('order'))
        item = order.orderitem_set.values('item__name',
                                          'item_ps',
                                          'item_id')
        discount = discount_percentages(order.total_price)
        if discount:
            order.discounts.add(Discount.objects.get(percent=discount))
        order.taxes.add(Tax.objects.get(percent=20))
        try:
            checkout_session = create_stripe_session(order,
                                                     items_ordered(item),
                                                     order.taxes.first(),
                                                     order.discounts.last()
                                                     )

            request.session['session_id'] = checkout_session.id
            request.session.save()
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)})


class PreviewCartView(View):
    """ Create Customer, Tax calculation and PaymentIntent. """

    def post(self, request, *args, **kwargs):
        try:

            order = Order.objects.get(id=request.session.get('order'))
            # Create Customer and PaymentIntent
            if not order.payment:
                # Get the customer's address from the request body
                address = json.loads(request.body)['address']
                # Create a tax calculation using the Stripe API
                calculation = create_tax_calculation(order, address)
                customer = create_customer(address)
                payment_intent = create_payment_intent(calculation=calculation,
                                                       order=order,
                                                       customer_id=customer[
                                                           'id']
                                                       )
                order.stripe_id = payment_intent.id
                order.save()

                request.session['payment_intent'] = payment_intent.id
                request.session.save()
                return JsonResponse(
                        {
                            'tax_amount': calculation['tax_amount_exclusive']
                            }
                        )
            else:
                messages.error(request, 'Order is paid')
                return render(request, 'error.html', {'messages': 'error'})
        except Order.DoesNotExist:
            messages.error(request, 'Order matching query does not exist')
            return render(request, 'error.html', {'messages': 'error'})

    def get(self, request, *args, **kwargs):
        payment_intent = retrieve_payment_intent(
                request.session.get('payment_intent')
                )
        payment_tax = retrieve_tax(payment_intent.metadata['tax_calculation'])

        return render(request,
                      'preview-cart.html',
                      {
                          'payment_tax': payment_tax,
                          'payment_intent': payment_intent,
                          'total_cost': payment_intent.amount / 100,
                          }
                      )


class ErrorView(View):
    """ Error view. Session clean. """

    def get(self, request, *args, **kwargs):
        clean_session(request.session)
        return render(request, 'error.html')


class PaymentSuccessView(View):
    """ Success view. Update order and session clean. """

    def get(self, request, *args, **kwargs):
        session = retrieve_stripe_session(request.session['session_id'])

        Order.objects.filter(pk=request.session['order']) \
            .update(payment=True, stripe_id=session.payment_intent)
        clean_session(request.session)
        return render(request,
                      'success.html',
                      {'name': session.customer_details.name})


class PaymentStatusView(View):
    """ Check status PaymentIntent. """

    def get(self, request, *args, **kwargs):
        status = request.GET.get('redirect_status')
        payment_id = request.GET.get('payment_intent')

        if status == 'succeeded' and \
                request.session.get('payment_intent') == payment_id:
            Order.objects.filter(pk=request.session.get('order')) \
                .update(payment=True, stripe_id=payment_id)
            clean_session(request.session)
            return render(request, 'success.html', status=201)
        return HttpResponse(200)


@csrf_exempt
def stripe_webhook(request):
    # stripe listen --forward-to localhost:8000/webhooks/stripe/
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
                )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    # Handle the checkout.session.completed event

    if event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']
        order_id = event['data']['object']['description']
        Order.objects.filter(pk=order_id).update(payment=True,
                                                 stripe_id=intent.id)

    elif event['type'] == "payment_intent.payment_failed":
        intent = event['data']['object']
        order_id = event['data']['object']['description']
        messages.error(request, intent.last_payment_error.message)
        return redirect('error')

    elif event['type'] == "payment_intent.canceled":
        intent = event['data']['object']
        order_id = event['data']['object']['description']
        messages.error(request, intent.failure_message)
        return redirect('error')

    return HttpResponse(status=200)
