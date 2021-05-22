from django.contrib import admin
from billing.models import PaymentTransaction, ItemPayment


class ItemPaymentModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'name': ('title',)}


admin.site.register(PaymentTransaction)
admin.site.register(ItemPayment, ItemPaymentModelAdmin)
