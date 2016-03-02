# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bba', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='city',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='building_No',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='country',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='street',
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='image',
            field=models.ImageField(default=b'MEDIA_ROOT', upload_to=b'profile_images', blank=True),
        ),
    ]
