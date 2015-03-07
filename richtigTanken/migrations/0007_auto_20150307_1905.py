# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('richtigTanken', '0006_auto_20150307_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpositions',
            name='zeit',
            field=models.DateTimeField(),
        ),
    ]
