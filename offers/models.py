from django.db import models
from account.models import User


class CardType:
    pass


class Achievement(models.Model):
    title = models.CharField(verbose_name='Название', max_length=220)
    description = models.TextField(verbose_name='Описание')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

    def __str__(self):
        return '{0}: {1}'.format(self.user.email, self.title)


class Card(models.Model):
    title = models.CharField(verbose_name='Название', max_length=220)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    card_type = models.CharField(verbose_name='Тип карты', max_length=220)
    balance = models.FloatField(verbose_name='Баланс', default=0)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.owner.email)
