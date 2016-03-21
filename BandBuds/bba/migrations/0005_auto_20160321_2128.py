# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bba', '0004_auto_20160321_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=b'Undisclosed', max_length=200, choices=[(b'Undisclosed', b'Undisclosed'), (b'Female', b'Female'), (b'Male', b'Male')]),
        ),
    ]
