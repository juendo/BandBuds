from django.db import models
class Band(models.Model):
    name 	= models.CharField(max_length=128, unique=False)
    city 	= models.CharField(max_length=128, unique=False)
    country = models.CharField(max_length=128, unique=False)
    formed 	= models.IntegerField(default=0)
    genre 	= models.CharField(max_length=128, unique=False)


class User(models.Model):
	user_id = models.CharField(max_length=128, unique=True)
	f_name	= models.CharField(max_length=128, unique=False)
	s_name  = models.CharField(max_length=128, unique=False)
	dob	= models.DateField(default=models.DateField.auto_now_add)
	smokes	= models.BooleanField()
	gender  = models.CharField(max_length=128, unique=False)
	alcohol = models.CharField(max_length=128, unique=False)

class Liked_Band(models.Model):
	band 	= models.ForeignKey(Band)
	yuser 	= models.ForeignKey(User)

#hello