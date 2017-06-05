# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

STATE_IN_PROCESS = 1
STATE_FINISHED = 2
STATE_ERROR = 3

STATE_CHOICES = (
    (STATE_IN_PROCESS, _('Search in process')),
    (STATE_FINISHED, _('Search is finished')),
    (STATE_ERROR, _('Search has errors')),
)


class OrdersFileList(models.Model):
    file_name = models.CharField(
        default=None, null=True, blank=True,
        max_length=120, verbose_name=_('Name of file with orders'))

    def __str__(self):
        return self.file_name


class ProductOrder(models.Model):
    product_url = models.CharField(
        default=None, null=True, blank=True,
        max_length=255, verbose_name=_('Product url'))
    product_name = models.IntegerField(
        default=None, null=True, blank=True,
        verbose_name=_('Product name'))
    status = models.SmallIntegerField(
        default=1, choices=STATE_CHOICES, verbose_name=_('Status of order'))
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))
    date_started = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date started'))

    def as_dict(self):
        return {
            'id': self.id,
            'product_url': self.product_url,
            'product_name': self.product_name,
            'status': self.status,
            'date_created': self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            'date_started': self.date_started.strftime("%Y-%m-%d %H:%M:%S"),
            'status_text': self.get_status_display(),
        }

    def __str__(self):
        return self.search_term
