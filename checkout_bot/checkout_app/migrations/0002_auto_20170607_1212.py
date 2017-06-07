# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='buyer_address',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Buyer address'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='buyer_city',
            field=models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Buyer city'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='buyer_postal_code',
            field=models.CharField(blank=True, default=None, max_length=25, null=True, verbose_name='Buyer postal code'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='buyer_state_code',
            field=models.CharField(blank=True, default=None, max_length=25, null=True, verbose_name='Buyer state code'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='orders_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkout_app.OrdersFileList', verbose_name='Orders file list instance'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='product_buyer',
            field=models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Product buyer'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='date_started',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date started'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='product_name',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Product name'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Product order created'), (2, 'Handling order'), (3, 'Order processed'), (4, 'Order processed with errors')], default=1, verbose_name='Status of order'),
        ),
    ]
