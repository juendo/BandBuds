# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bba', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dances',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='involvement',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(default=datetime.date(2016, 3, 19)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=b'U', max_length=1, choices=[(b'U', b'Undisclosed'), (b'F', b'Female'), (b'M', b'Male')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='smokes',
            field=models.IntegerField(default=0),
        ),
    ]
