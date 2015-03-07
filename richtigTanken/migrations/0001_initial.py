# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BenzinPreis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preis', models.DecimalField(max_digits=5, decimal_places=2)),
                ('start_zeit', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FahrtDaten',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('strecken_laengekm', models.DecimalField(max_digits=4, decimal_places=1)),
                ('spritverbrauch_in_l', models.IntegerField()),
                ('start_zeit', models.DateTimeField()),
                ('end_zeit', models.DateTimeField()),
                ('nutzer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tankstellen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bezeichnung', models.CharField(max_length=256)),
                ('x_wert', models.IntegerField()),
                ('y_wert', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='benzinpreis',
            name='tankstelle',
            field=models.ForeignKey(to='richtigTanken.Tankstellen'),
            preserve_default=True,
        ),
    ]
