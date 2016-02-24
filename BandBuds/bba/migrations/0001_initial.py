# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bba.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('country', models.CharField(max_length=128)),
                ('formed', models.IntegerField(default=0)),
                ('genre', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Buddy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Disliked_Bands',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band', models.ForeignKey(to='bba.Band')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('band', models.ForeignKey(to='bba.Band')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gig_Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gig', models.CharField(max_length=30, verbose_name=bba.models.Gig)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Liked_Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band', models.ForeignKey(to='bba.Band')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Performing_Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band', models.ForeignKey(to='bba.Band')),
                ('gig', models.ForeignKey(to='bba.Gig')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.CharField(unique=True, max_length=128)),
                ('f_Name', models.CharField(max_length=128)),
                ('s_Name', models.CharField(max_length=128)),
                ('dob', models.DateField()),
                ('smokes', models.BooleanField(default=None)),
                ('gender', models.CharField(max_length=128)),
                ('drinks', models.BooleanField(default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('venue_id', models.IntegerField(default=0)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('postcode', models.CharField(max_length=50)),
                ('building_No', models.IntegerField(default=0)),
                ('street', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='liked_band',
            name='user',
            field=models.ForeignKey(to='bba.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gig_attendance',
            name='user',
            field=models.ForeignKey(to='bba.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gig',
            name='venue',
            field=models.ForeignKey(to='bba.Venue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='disliked_bands',
            name='user',
            field=models.ForeignKey(to='bba.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buddy',
            name='buddy',
            field=models.ForeignKey(to='bba.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buddy',
            name='user',
            field=models.OneToOneField(related_name=b'+', to='bba.User'),
            preserve_default=True,
        ),
    ]
