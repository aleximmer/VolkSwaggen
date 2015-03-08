# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('richtigTanken', '0008_auto_20150307_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='tankstellen',
            name='preis',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
    ]
