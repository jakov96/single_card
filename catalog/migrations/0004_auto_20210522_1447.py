# Generated by Django 2.2 on 2021-05-22 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('catalog', '0003_auto_20210522_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='address',
        ),
        migrations.RemoveField(
            model_name='service',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='service',
            name='site',
        ),
        migrations.AddField(
            model_name='service',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Organization', verbose_name='Организация'),
        ),
    ]