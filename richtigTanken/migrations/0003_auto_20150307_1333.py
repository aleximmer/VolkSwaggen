# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('richtigTanken', '0002_userpositions'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpositions',
            name='benzin_delta_in_l',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fahrtdaten',
            name='spritverbrauch_in_l',
            field=models.DecimalField(max_digits=4, decimal_places=2),
        ),
    ]
