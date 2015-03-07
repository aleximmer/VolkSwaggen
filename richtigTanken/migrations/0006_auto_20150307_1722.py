# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('richtigTanken', '0005_auto_20150307_1416'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='benzinpreis',
            options={'ordering': ('start_zeit',)},
        ),
        migrations.AlterModelOptions(
            name='fahrtdaten',
            options={'ordering': ('end_zeit',)},
        ),
        migrations.AlterModelOptions(
            name='userpositions',
            options={'ordering': ('zeit',)},
        ),
    ]
