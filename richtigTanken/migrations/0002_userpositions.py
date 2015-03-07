# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('richtigTanken', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPositions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zeit', models.DateTimeField(auto_now=True)),
                ('position_x', models.IntegerField()),
                ('position_y', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
