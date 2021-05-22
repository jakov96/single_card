# Generated by Django 2.2 on 2021-05-22 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_achievement_logo'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='achievements',
            field=models.ManyToManyField(blank=True, to='catalog.Achievement', verbose_name='Достижения'),
        ),
    ]
