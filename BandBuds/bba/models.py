from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.core.validators import validate_email
from django.template.defaultfilters import slugify
from datetime import date

# choices for the gender data field
GENDER_CHOICES = (
    ('Undisclosed', 'Undisclosed'),
    ('Female', 'Female'),
    ('Male', 'Male'),
)

class UserProfile(models.Model):

    # Django defined User class
    user = models.OneToOneField(User)

    # additional fields for UserProfile (all given default values)
    dob = models.DateField(default=date.today())
    gender = models.CharField(default="Undisclosed", max_length=200, choices=GENDER_CHOICES)
    smokes = models.IntegerField(default=0)
    drinks = models.IntegerField(default=0)
    dances = models.IntegerField(default=0)
    involvement = models.IntegerField(default=0)

    image = models.ImageField(upload_to='profile_images',blank=True,default='profile_images/default_image.png')
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

class Band(models.Model):
    # stores name of band and URL to image of band from Songkick website
    name = models.CharField(max_length=128, unique=False)
    image_Ref = models.CharField(max_length=128, unique=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
         self.slug = slugify(self.name)
         super(Band, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class LikedBand(models.Model):
    # links a Band and UserProfile object
    band = models.ForeignKey(Band)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return str(self.band) + ' ' + str(self.user)

class DisLikedBand(models.Model):
    # links a Band and UserProfile object
    band = models.ForeignKey(Band)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.band + ' ' + self.user

class Venue(models.Model):
    # venue information
    venue_id = models.IntegerField(default=0)
    name = models.CharField(max_length=128)
    # latitude and logitude?

    def __unicode__(self):
        return self.name

class Gig(models.Model):
    # gig information
    gig_id = models.IntegerField(default=0)
    date = models.DateField()
    time = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    venue = models.ForeignKey(Venue)
    band = models.ForeignKey(Band)

    def __unicode__(self):
        return self.venue.name + ' ' + self.band.name

class PerformingBand(models.Model):
    # links a Band to a Gig object
    band = models.ForeignKey(Band)
    gig = models.ForeignKey(Gig)

    def __unicode__(self):
        return self.band + self.gig

class GigAttendance(models.Model):
    # links a Gig to a UserProfile object
    gig = models.ForeignKey(Gig)
    user = models.ForeignKey(UserProfile)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(GigAttendance, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.gig.band.name + ' ' + self.user.user.username


class Buddy(models.Model):
    # links two UserProfile objects
    # this represents a 'buddy request' state
    # if accept is set to true, the request is accepted and
    # the two UserProfiles are deemed to be 'buddies'
    user = models.ForeignKey(UserProfile)
    # as we have two UserProfile foreign keys one must be unique
    # a user can have multiple buddy links, but each buddy must be unique
    buddy = models.ForeignKey(UserProfile, related_name='+')
    gig = models.ForeignKey(Gig)
    accept = models.BooleanField(default=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
         self.slug = slugify(self.user)
         super(Buddy, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user + ' ' + self.buddy + ' ' + self.gig.band + ' request accepted: ' + self.accept