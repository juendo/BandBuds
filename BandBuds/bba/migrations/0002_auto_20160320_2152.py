# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bba', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buddy',
            name='buddy',
            field=models.ForeignKey(related_name=b'+', to='bba.UserProfile'),
        ),
        migrations.AlterField(
            model_name='buddy',
            name='user',
            field=models.ForeignKey(to='bba.UserProfile'),
        ),
    ]
