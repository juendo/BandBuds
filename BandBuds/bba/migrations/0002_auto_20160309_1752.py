# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bba', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GigAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('gig', models.ForeignKey(to='bba.Gig')),
                ('user', models.ForeignKey(to='bba.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Disliked_Bands',
            new_name='DisLikedBands',
        ),
        migrations.RenameModel(
            old_name='Liked_Band',
            new_name='LikedBand',
        ),
        migrations.RenameModel(
            old_name='Performing_Band',
            new_name='PerformingBand',
        ),
        migrations.RemoveField(
            model_name='gig_attendance',
            name='gig',
        ),
        migrations.RemoveField(
            model_name='gig_attendance',
            name='user',
        ),
        migrations.DeleteModel(
            name='Gig_Attendance',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(default=datetime.date(2016, 3, 9)),
        ),
    ]
