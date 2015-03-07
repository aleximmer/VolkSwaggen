# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('richtigTanken', '0004_auto_20150307_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tankstellen',
            name='x_wert',
        ),
        migrations.RemoveField(
            model_name='tankstellen',
            name='y_wert',
        ),
        migrations.AddField(
            model_name='tankstellen',
            name='position_x',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tankstellen',
            name='position_y',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=6),
            preserve_default=False,
        ),
    ]
