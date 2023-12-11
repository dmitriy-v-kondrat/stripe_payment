import uuid

from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

# Create your models here.

CURRENCY_CHOICES = [
    ('$', 'usd'),
    ('€', 'eur'),
    ]


class Order(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False
                          )
    stripe_id = models.CharField(max_length=255,
                                 null=True,
                                 blank=True
                                 )
    payment = models.BooleanField(default=False)
    total_price = models.PositiveSmallIntegerField(default=0,
                                                   verbose_name='Price '
                                                                'without '
                                                                'discount')
    pay_currency = models.CharField(max_length=4,
                                    choices=CURRENCY_CHOICES,
                                    default='usd'
                                    )
    items = models.ManyToManyField('Item',
                                   related_name='orders',
                                   blank=True,
                                   through='OrderItem'
                                   )

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('order', kwargs={'pk': self.pk})


class Discount(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              related_name='discounts',
                              )
    percent = models.PositiveSmallIntegerField(default=0,
                                               validators=
                                               [MaxValueValidator(99)],
                                               verbose_name='Discount %',
                                               )

    def __str__(self):
        return str(self.percent)


class Tax(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              related_name='taxes'
                              )
    percent = models.PositiveSmallIntegerField(default=0,
                                               validators=
                                               [MaxValueValidator(99)]
                                               )

    def __str__(self):
        return str(self.percent)


class Item(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.PositiveSmallIntegerField(default=0)
    currency = models.CharField(max_length=4,
                                choices=CURRENCY_CHOICES,
                                default='usd'
                                )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_ps = models.PositiveSmallIntegerField(default=0)
