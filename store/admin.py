from django.contrib import admin

from store.models import Discount, Item, Order, Tax


class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 0
    readonly_fields = ('percent',)


class ItemAdmin(admin.ModelAdmin):
    model = Item


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        DiscountInline
        ]
    model = Order
    readonly_fields = ('stripe_id',
                       'payment',
                       'total_price',
                       'pay_currency',
                       'items',
                       )


class DiscountAdmin(admin.ModelAdmin):
    model = Discount


class TaxAdmin(admin.ModelAdmin):
    model = Tax


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)
