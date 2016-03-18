from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.core.validators import validate_email
from django.template.defaultfilters import slugify
from datetime import date

GENDER_CHOICES = (
    ('U', 'Undisclosed'),
    ('F', 'Female'),
    ('M', 'Male'),
)

DRINKS_CHOICES = (
    ('U', 'Undisclosed'),
    ('A', 'I do not Drink'),
    ('P', 'I like to party'),
    ('Z', 'I like to party alot'),
)

SMOKES_CHOICES = (
    ('1', 'Undisclosed'),
    ('2', 'I do not smoke'),
    ('3', 'I am partial to a smoke'),
    ('4', 'I like to smoke alot')
)
class UserProfile(models.Model):

    user = models.OneToOneField(User)
    dob = models.DateField(default=date.today())
    smokes = models.BooleanField(default=False, choices=SMOKES_CHOICES)
    gender = models.CharField(default="U", max_length=1, choices=GENDER_CHOICES)
    drinks = models.CharField(default="U", max_length=1, choices=DRINKS_CHOICES)
    image = models.ImageField(upload_to='profile_images',blank=True,default='profile_images/default_image.png')
    slug = models.SlugField()

    def save(self, *args, **kwargs):
         self.slug = slugify(self.user)
         super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

class Band(models.Model):
    name = models.CharField(max_length=128, unique=False)
    image_Ref = models.CharField(max_length=128, unique=False)

    def __unicode__(self):
        return self.name

class LikedBand(models.Model):
    band = models.ForeignKey(Band)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return str(self.band) + ' ' + str(self.user)

class DisLikedBands(models.Model):
    band = models.ForeignKey(Band)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.band + ' ' + self.user

class Buddy(models.Model):
    user = models.OneToOneField(UserProfile, related_name='+')
    buddy = models.ForeignKey(UserProfile)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
         self.slug = slugify(self.user)
         super(Buddy, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.UserProfile + ' buddied with ' + self.buddy

class Venue(models.Model):
    venue_id = models.IntegerField(default=0)
    name = models.CharField(max_length=128)
    # latitude and logitude?

    def __unicode__(self):
        return self.name

class Gig(models.Model):
    gig_id = models.IntegerField(default=0)
    date = models.DateField()
    time = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    venue = models.ForeignKey(Venue)
    band = models.ForeignKey(Band)

    def __unicode__(self):
        return self.venue.name + ' ' + self.band.name

class PerformingBand(models.Model):
    band = models.ForeignKey(Band)
    gig = models.ForeignKey(Gig)

    def __unicode__(self):
        return self.band + self.gig

class GigAttendance(models.Model):
    gig = models.ForeignKey(Gig)
    user = models.ForeignKey(UserProfile)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(GigAttendance, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.gig.band.name + ' ' + self.user.user.username

class Nudge(models.Model):
    nudger = models.ForeignKey(User)
    nudgee = models.ForeignKey(UserProfile)
    gig = models.ForeignKey(Gig)

    def __unicode__(self):
        return nudger.user.username + ' nudged ' + nudgee.user.username + ' about ' + gig 