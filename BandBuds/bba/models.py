from django.db import models

class User(models.Model):
	user_id     = models.CharField(max_length=128, unique=True)
	f_Name	    = models.CharField(max_length=128, unique=False)
	s_Name      = models.CharField(max_length=128, unique=False)
	dob	        = models.DateField(default=models.DateField.auto_now_add)
	smokes	    = models.BooleanField()
	gender      = models.CharField(max_length=128, unique=False)
	alcohol     = models.BooleanField()

    def __unicode__(self):
        return self.user_id


class Buddy(models.model):
    user_Id     = models.CharField(primary_key=True,max_length=50)
    user_Id     = models.ForeignKey("user_Id")

 def __unicode__(self):
        return 

class Band(models.Model):
    name 	    = models.CharField(primary_key=True, max_length=50)
    city 	    = models.CharField(primary_key=True, max_length=50)
    country     = models.CharField(primary_key=True, max_length=50)
    formed 	    = models.IntegerField(default=0)
    genre 	    = models.CharField(max_length=25)

      def __unicode__(self):
        return self.name + ' ' + self.city + ' ' + self.country

class Liked_Band(models.model):
    name        = models.ForeignKey(Name, max_length=50)
    city        = models.ForeignKey(City, max_length=50)
    country     = models.ForeignKey(Country, max_length=50)

    def __unicode__(self):
        return 


class Performing_Band(models.model):
    name        = models.ForeignKey(Name, max_length=50)
    city        = models.ForeignKey(City, max_length=50)
    country     = models.ForeignKey(Country, max_length=50)
    gig_Id      = models.ForeignKey(Gig_Id, max_length=50, unique=True)

 def __unicode__(self):
        return 

class Gig(models.model):
    date        = models.DateField(default=models.DateField.auto_now_add)
    time        = models.DateField(default=models.DateField.auto_now_add)
    country     = models.ForeignKey(Country, max_length=128, unique=True)
    city        = models.ForeignKey(City, max_length=128, unique=True)
    venue_Id    = models.ForeignKey(Venue_Id, max_length=128, unique=True)
    band_Name   = models.ForeignKey(Band_Name, max_length=128)

 def __unicode__(self):
        return 

class Gig_Attendance(models.model):
    gig_Id      = models.CharField(primary_key=True, max_length=50)
    user_Id     = models.ForeignKey(User_Id, max_length=128, unique=True)

 def __unicode__(self):
        return 

class Venue(models.model):
    city        = models.CharField(max_length=50)
    country     = models.CharField(max_length=50)
    postcode    = models.CharField(max_length=50)
    building_No = models.IntegerField(default=0)
    street      = models.CharField(max_length=128)

 def __unicode__(self):
        return self.name
