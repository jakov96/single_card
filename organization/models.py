from django.db import models
from catalog.models import Service


class Organization(models.Model):
    inn = models.CharField(verbose_name='ИНН', max_length=200, unique=True)
    title = models.CharField(verbose_name='Название', max_length=200)
    address = models.CharField(verbose_name='Адрес', max_length=200)
    phone = models.CharField(verbose_name='Телефон', max_length=20, null=True, blank=True)
    site = models.CharField(verbose_name='Сайт', max_length=200, null=True, blank=True)
    is_confirm = models.NullBooleanField(verbose_name='Подтвержденная организация', null=True, blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.title

    def get_services(self):
        return Service.objects.filter(organization=self)