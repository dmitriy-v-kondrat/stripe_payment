

from django.urls import path

from store.views import (CheckoutView, ErrorView,
                         ItemDetailView,
                         ItemListView,
                         OrderCreateView,
                         OrderDetailView,
                         PaymentStatusView,
                         PaymentSuccessView,
                         stripe_config,
                         stripe_webhook,
                         PreviewCartView,
                         )

urlpatterns = [
    path('item-list/', ItemListView.as_view(), name='items'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('add-order/<int:pk>/', OrderCreateView.as_view(), name='add_order'),
    path('order/<uuid:pk>/', OrderDetailView.as_view(), name='order'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('preview-cart/', PreviewCartView.as_view(), name='preview-cart'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('error/', ErrorView.as_view(), name='error'),
    path('paymentstatus/', PaymentStatusView.as_view(), name='intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('config/', stripe_config)
]
