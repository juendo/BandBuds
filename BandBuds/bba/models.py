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
    f_name = models.CharField(max_length=128, unique=False)
    s_name = models.CharField(max_length=128, unique=False)
    dob = models.DateField()
    smokes = models.BooleanField(default=None)
    gender = models.CharField(max_length=128, unique=False)
    alcohol = models.CharField(max_length=128, unique=False)

    def __unicode__(self):
        return self.user_id


class Liked_Band(models.Model):
    band = models.ForeignKey(Band)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.band) + ' ' + str(self.user)

        # hello
