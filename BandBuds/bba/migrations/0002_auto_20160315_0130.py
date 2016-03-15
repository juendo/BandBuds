# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bba', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nudge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gig', models.ForeignKey(to='bba.Gig')),
                ('nudgee', models.ForeignKey(to='bba.UserProfile')),
                ('nudger', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(default=datetime.date(2016, 3, 15)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=b'Undisclosed', max_length=128),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='smokes',
            field=models.BooleanField(default=False),
        ),
    ]
