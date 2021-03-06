from django.db import models
from catalog.models import Service


class TransactionTypes:
    replenishment = 'replenishment'
    consumption = 'consumption'

    names = {
        replenishment: 'Приход',
        consumption: 'Расход'
    }

    choices = (
        (replenishment, names[replenishment]),
        (consumption, names[consumption])
    )


class PaymentTypes:
    card = 'card'
    phone_number = 'phone_number'

    names = {
        card: 'Банковская карта',
        phone_number: 'По номеру телефона'
    }

    choices = (
        (card, names[card]),
        (phone_number, names[phone_number]),
    )


class ItemPayment(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    name = models.SlugField(help_text='Сгенерируется автоматически', unique=True)

    class Meta:
        verbose_name = 'Статья транзакции'
        verbose_name_plural = 'Статьи транзакций'

    def __str__(self):
        return self.title


class PaymentTransaction(models.Model):
    transaction_type = models.CharField(verbose_name='Тип транзакции', choices=TransactionTypes.choices, max_length=200)
    transaction_sum = models.FloatField(verbose_name='Сумма')
    description = models.TextField(verbose_name='Описание')
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    user = models.ForeignKey('account.User', verbose_name='Пользователь', on_delete=models.CASCADE)
    item_payment = models.ForeignKey(ItemPayment, verbose_name='Статья транзакции', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return '{0} {1}'.format(self.transaction_type, self.transaction_sum)

    def get_transaction_type(self):
        return self.transaction_type


class UserPaymentOrder(models.Model):
    user = models.ForeignKey('account.User', verbose_name='Пользователь', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE)
    date_start = models.DateTimeField(verbose_name='Дата и время', auto_now_add=True)
    is_paid = models.BooleanField(verbose_name='Оплачен?', default=False)
    is_canceled = models.BooleanField(verbose_name='Отменен?', default=False)

    class Meta:
        verbose_name = 'Заказ для оплаты'
        verbose_name_plural = 'Заказы для оплаты'
