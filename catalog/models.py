from django.db import models
from imagemanager.models import BaseImage


class Achievement(models.Model):
    title = models.CharField(verbose_name='Название', max_length=220)
    description = models.TextField(verbose_name='Описание')
    logo = models.ForeignKey('imagemanager.BaseImage', verbose_name='Лого', null=True, blank=True,
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

    def __str__(self):
        return self.title

    def get_logo(self):
        return self.logo.image_min


class Card(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    owner = models.ForeignKey('account.User', verbose_name='Владелец', on_delete=models.CASCADE)
    card_type = models.CharField(verbose_name='Тип карты', max_length=200)
    balance = models.FloatField(verbose_name='Баланс', default=0)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.owner.email)


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(help_text='Сгенерируется автоматически', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_count_service(self):
        return self.service_set.count()

    def get_services(self):
        return Service.objects.filter(category=self)


class Service(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(help_text='Сгенерируется автоматически', unique=True)
    organization = models.ForeignKey('organization.Organization', verbose_name='Организация', null=True, blank=True,
                                     on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    is_free = models.BooleanField(verbose_name='Бесплатная услуга?', default=False)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title
