from django.db import models

class User(models.Model):
	user_id     = models.CharField(primary_key=True)
	f_Name	    = models.CharField(max_length=128, unique=False)
	s_Name      = models.CharField(max_length=128, unique=False)
	dob	        = models.DateField(default=models.DateField.auto_now_add)
	smokes	    = models.BooleanField()
	gender      = models.CharField(max_length=128, unique=False)
	alcohol     = models.BooleanField()
    email       = models.EmailField(max_length=254)

    def __unicode__(self):
        return self.user_id


class Buddy(models.model):
    user_Id     = models.CharField(primary_key=True)
    user_Id     = models.ForeignKey(user_Id)

    def __unicode__(self):
        return self.user_id

class Band(models.Model):
    name 	    = models.CharField(primary_key=True)
    city 	    = models.CharField(primary_key=True)
    country     = models.CharField(primary_key=True)
    formed 	    = models.IntegerField(default=0)
    genre 	    = models.CharField(max_length=25)

      def __unicode__(self):
        return self.name + ' ' + self.city + ' ' + self.country

class Liked_Band(models.model):
    name        = models.ForeignKey(Name)
    city        = models.ForeignKey(City)
    country     = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name


class Performing_Band(models.model):
    name        = models.ForeignKey(Name)
    city        = models.ForeignKey(City)
    country     = models.ForeignKey(Country)
    gig_Id      = models.ForeignKey(Gig_Id)

    def __unicode__(self):
        return self.gig_Id

class Gig(models.model):
    date        = models.DateField(default=models.DateField.auto_now_add)
    time        = models.DateField(default=models.DateField.auto_now_add)
    country     = models.ForeignKey(Country)
    city        = models.ForeignKey(City)
    venue_Id    = models.ForeignKey(Venue_Id)
    band_Name   = models.ForeignKey(Band_Name)

    def __unicode__(self):
        return self.band_Name

class Gig_Attendance(models.model):
    gig_Id      = models.CharField(primary_key=True)
    user_Id     = models.ForeignKey(User_Id)

    def __unicode__(self):
        return self.gig_Id

class Venue(models.model):
    city        = models.CharField(max_length=50)
    country     = models.CharField(max_length=50)
    postcode    = models.CharField(max_length=50)
    building_No = models.IntegerField(default=0)
    street      = models.CharField(max_length=128)

    def __unicode__(self):
        return self.street
