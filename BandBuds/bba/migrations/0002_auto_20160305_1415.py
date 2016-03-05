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
            model_name='gig',
            name='gig_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='dob',
            field=models.DateField(default=datetime.date(2016, 3, 5)),
        ),
    ]
