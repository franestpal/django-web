from django.contrib import admin

from .models2 import Item, OrderItem, Order, Payment, Coupon, Refund, BillingAddress, Category, Slide


# Register your models here.


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = [

                    ]
    list_display_links = [
       
    ]
    list_filter = [
                   
                   ]
    search_fields = [

    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = [ 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


def copy_items(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


copy_items.short_description = 'Copy Items'


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['title', 'category']
    actions = [copy_items]

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'is_active']


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Slide)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(BillingAddress, AddressAdmin)
