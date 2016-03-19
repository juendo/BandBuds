# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('image_Ref', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Buddy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisLikedBands',
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
                ('gig_id', models.IntegerField(default=0)),
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
            name='GigAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('gig', models.ForeignKey(to='bba.Gig')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LikedBand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band', models.ForeignKey(to='bba.Band')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nudge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gig', models.ForeignKey(to='bba.Gig')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PerformingBand',
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
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dob', models.DateField(default=datetime.date(2016, 3, 19))),
                ('gender', models.CharField(default=b'U', max_length=1, choices=[(b'U', b'Undisclosed'), (b'F', b'Female'), (b'M', b'Male')])),
                ('smokes', models.IntegerField(default=0)),
                ('drinks', models.IntegerField(default=0)),
                ('dances', models.IntegerField(default=0)),
                ('involvement', models.IntegerField(default=0)),
                ('image', models.ImageField(default=b'profile_images/default_image.png', upload_to=b'profile_images', blank=True)),
                ('slug', models.SlugField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
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
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nudge',
            name='nudgee',
            field=models.ForeignKey(to='bba.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nudge',
            name='nudger',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='likedband',
            name='user',
            field=models.ForeignKey(to='bba.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gigattendance',
            name='user',
            field=models.ForeignKey(to='bba.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gig',
            name='venue',
            field=models.ForeignKey(to='bba.Venue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dislikedbands',
            name='user',
            field=models.ForeignKey(to='bba.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buddy',
            name='buddy',
            field=models.ForeignKey(to='bba.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buddy',
            name='user',
            field=models.OneToOneField(related_name=b'+', to='bba.UserProfile'),
            preserve_default=True,
        ),
    ]
