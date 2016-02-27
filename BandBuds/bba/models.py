from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Member(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    dob = models.DateField()
    smokes = models.BooleanField(default=None)
    gender = models.CharField(max_length=128, unique=False)
    drinks = models.BooleanField(default=None)
    first_name = models.CharField(max_length=40, unique=True)
    last_name = models.CharField(max_length=40, unique=True)

def __unicode__(self):
    return self.username

class Band(models.Model):
    name = models.CharField(max_length=128, unique=False)
    image_Ref = models.CharField(max_length=128, unique=False)

    def __unicode__(self):
        return self.name

class Liked_Band(models.Model):
    band = models.ForeignKey(Band)
    member = models.ForeignKey(Member)

    def __unicode__(self):
        return str(self.band) + ' ' + str(self.member)

class Buddy(models.Model):
    user = models.OneToOneField(Member,related_name='+')
    buddy = models.ForeignKey(Member)

    def __unicode__(self):
        return self.member + ' buddied with ' + self.buddy


class Venue(models.Model):
    venue_id = models.IntegerField(default=0)
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    postcode = models.CharField(max_length=128)
    building_No = models.IntegerField(default=128)
    street = models.CharField(max_length=128)

    def __unicode__(self):
        return self.city + ' ' + self.street

class Gig(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    venue = models.ForeignKey(Venue)
    band = models.ForeignKey(Band)

    def __unicode__(self):
        return self.venue + ' ' + self.band


class Performing_Band(models.Model):
    band = models.ForeignKey(Band)
    gig = models.ForeignKey(Gig)

    def __unicode__(self):
        return self.band + self.gig


class Disliked_Bands(models.Model):
    band = models.ForeignKey(Band)
    member = models.ForeignKey(Member)

    def __unicode__(self):
        return self.band + ' ' + self.member


class Gig_Attendance(models.Model):
    gig = models.CharField(Gig,max_length=30)
    member = models.ForeignKey(Member)

    def __unicode__(self):
        return self.gig + ' ' + self.member
