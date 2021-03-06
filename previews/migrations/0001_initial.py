# Generated by Django 2.0.2 on 2019-01-04 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preview',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='commerce.Item')),
                ('mode', models.CharField(choices=[('monthly', 'Месяц'), ('weekly', 'Неделя')], max_length=8, null=True, verbose_name='Тип')),
                ('title_origin', models.CharField(blank=True, default='Без названия', max_length=512, verbose_name='Оригинальное название')),
                ('diamond_id', models.CharField(max_length=9, null=True, verbose_name='ID Diamond')),
                ('release_date', models.DateField(null=True, verbose_name='Дата выхода')),
                ('session', models.BigIntegerField(null=True, verbose_name='Сессия')),
                ('midtown_id', models.CharField(max_length=64, null=True, verbose_name='Код Midtown')),
                ('cover_origin', models.URLField(blank=True, default='', null=True, verbose_name='Оригинальнаый адрес обложки')),
                ('price_map', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commerce.PriceMap', verbose_name='Таблица цен')),
            ],
            options={
                'verbose_name': 'Предзаказ',
                'verbose_name_plural': 'Предзаказы',
            },
            bases=('commerce.item',),
        ),
    ]
