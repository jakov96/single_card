# Generated by Django 2.2 on 2021-05-22 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('name', models.SlugField(help_text='Сгенерируется автоматически', unique=True)),
            ],
            options={
                'verbose_name': 'Статья транзакции',
                'verbose_name_plural': 'Статьи транзакций',
            },
        ),
        migrations.CreateModel(
            name='UserPaymentOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачен?')),
                ('is_canceled', models.BooleanField(default=False, verbose_name='Отменен?')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Service', verbose_name='Услуга')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ для оплаты',
                'verbose_name_plural': 'Заказы для оплаты',
            },
        ),
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('replenishment', 'Приход'), ('consumption', 'Расход')], max_length=200, verbose_name='Тип транзакции')),
                ('transaction_sum', models.FloatField(verbose_name='Сумма')),
                ('description', models.TextField(verbose_name='Описание')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('item_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.ItemPayment', verbose_name='Статья транзакции')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
            },
        ),
    ]
