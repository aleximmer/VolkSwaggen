# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('richtigTanken', '0007_auto_20150307_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fahrtdaten',
            name='strecken_laengekm',
            field=models.DecimalField(max_digits=5, decimal_places=1),
        ),
    ]
