from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=128, unique=False)
    city = models.CharField(max_length=128, unique=False)
    country = models.CharField(max_length=128, unique=False)
    formed = models.IntegerField(default=0)
    genre = models.CharField(max_length=128, unique=False)

    def __unicode__(self):
        return self.name + ' ' + self.city + ' ' + self.country


class User(models.Model):
    user_id = models.CharField(max_length=128, unique=True)
    f_Name = models.CharField(max_length=128, unique=False)
    s_Name = models.CharField(max_length=128, unique=False)
    dob = models.DateField()
    smokes = models.BooleanField(default=None)
    gender = models.CharField(max_length=128, unique=False)
    drinks = models.BooleanField(default=None)

    def __unicode__(self):
        return self.user_id


class Liked_Band(models.Model):
    band = models.ForeignKey(Band)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.band) + ' ' + str(self.user)




class Buddy(models.Model):
    user = models.OneToOneField(User,related_name='+')
    buddy = models.ForeignKey(User)

    def __unicode__(self):
        return self.user + ' buddied with ' + self.buddy



class Venue(models.Model):
    venue_id = models.IntegerField(default=0)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    building_No = models.IntegerField(default=0)
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
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.band + ' ' + self.user


class Gig_Attendance(models.Model):
    gig = models.CharField(Gig,max_length=30)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.gig + ' ' + self.user



