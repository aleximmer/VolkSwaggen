# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('richtigTanken', '0003_auto_20150307_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpositions',
            name='position_x',
            field=models.DecimalField(max_digits=8, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='userpositions',
            name='position_y',
            field=models.DecimalField(max_digits=8, decimal_places=6),
        ),
    ]
