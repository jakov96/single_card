# Generated by Django 2.2 on 2021-05-22 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Изображение')),
                ('image_min', models.CharField(blank=True, default='', editable=False, max_length=250)),
                ('image_middle', models.CharField(blank=True, default='', editable=False, max_length=250)),
                ('image_large', models.CharField(blank=True, default='', editable=False, max_length=250)),
                ('alt', models.CharField(blank=True, default='', max_length=250, verbose_name='Тег alt')),
                ('width', models.IntegerField(blank=True, null=True, verbose_name='Ширина')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='Высота')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]
