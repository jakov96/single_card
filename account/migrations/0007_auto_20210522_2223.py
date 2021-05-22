# Generated by Django 2.2 on 2021-05-22 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_userregistrationconfirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('guest', 'Гость'), ('citizen', 'Житель')], default='citizen', max_length=120, null=True, verbose_name='Тип пользоватля'),
        ),
    ]
