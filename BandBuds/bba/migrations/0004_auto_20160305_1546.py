# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bba', '0003_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig_attendance',
            name='gig',
            field=models.ForeignKey(to='bba.Gig'),
        ),
    ]
