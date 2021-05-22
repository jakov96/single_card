from pytils.translit import slugify
from billing.models import ItemPayment, PaymentTransaction, TransactionTypes


class PaymentTransactionManager:
    @classmethod
    def get_or_create_item_payment(cls, title):
        """
        Получение или создания статьи транзакции
        :param title:
        :return:
        """
        item_payment = ItemPayment.objects.filter(title=title).first()
        if not item_payment:
            name = slugify(title)
            item_payment = ItemPayment(title=title, name=name)
            item_payment.save()
        return item_payment

    @classmethod
    def recharge(cls, user, transaction_sum):
        """
        Пополнение баланса
        :param user:
        :param transaction_sum:
        :return:
        """
        item_payment = cls.get_or_create_item_payment('Пополнение баланса')
        return PaymentTransaction.objects.create(transaction_type=TransactionTypes.replenishment,
                                                 user=user,
                                                 item_payment=item_payment,
                                                 transaction_sum=transaction_sum,
                                                 description='Пополнение баланса')

    @classmethod
    def get_balance(cls, user):
        """
        Расчет баланса
        :param user:
        :return:
        """
        transactions = PaymentTransaction.objects.filter(user=user)
        replenishment_sum = sum([transaction.transaction_sum for transaction in transactions if
                                 transaction.transaction_type == TransactionTypes.replenishment])
        consumption_sum = sum([transaction.transaction_sum for transaction in transactions if
                               transaction.transaction_type == TransactionTypes.consumption])
        return replenishment_sum - consumption_sum
