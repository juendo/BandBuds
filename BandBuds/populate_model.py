#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BandBuds.settings')

import json
import urllib
import urllib2
from datetime import date
from django.core.validators import validate_email
import django
django.setup()
from django.core.validators import validate_email

from bba.models import Band, UserProfile, LikedBand, Gig, Venue, GigAttendance

from django.contrib.auth.models import User

API_KEY = "jwzmbEyCAIwD7HCy"

def populate():

    #added in users for presentation
    # Creating mock users
    stevo_user = add_user('steve','e@m.ail','123')
    neil_user = add_user('neil','neil@hotmail.com', '123')
    anaJ_user = add_user('Ana Jahnke','ana_jahnke@hotmail.com','123')
    lewis_user = add_user('Lewis','l@hotmail.com','123')
    gladis_user = add_user('Gladis','glad@hotmail.com','123')
    joel_user = add_user('Joel','joel@me.com','123')
    rob_user = add_user('Rob','Rob@hotmail.com','123')
    mario_user = add_user('Mario','mario@hotmail.com','123')
    polly_user = add_user('Polly','poll@hotmail.com','123')
    david_user = add_user('david','david@hotmail.com','123')
    laura_user = add_user('laura','laura@hotmail.com','123')
    leifos_user = add_user('leifos','leifos@hotmail.com','123')

    # Create profile
    stevo_profile = add_profile(stevo_user,date(1983,1,26),'Male',0,4,4,3)
    neil_profile = add_profile(neil_user,date(1992,3,16), 'Male',3,2,3,4)
    lewis_profile = add_profile(lewis_user,date(1990,1,14),'Male',0,0,1,1)
    anaJ_profile = add_profile(anaJ_user,date(1950,2,26),'Male',0,1,1,4)
    gladis_profile = add_profile(gladis_user,date(1950,2,26),'Female',1,1,3,2)
    joel_profile = add_profile(joel_user,date(1983,11,07),'Male',4,4,4,4)
    rob_profile = add_profile(rob_user,date(1984,8,30),'Male',1,4,3,3)
    mario_profile = add_profile(mario_user,date(1984,3,26),'Male',2,1,3,1)
    polly_profile = add_profile(polly_user,date(1982,5,26),'Female',3,1,2,4)
    david_profile = add_profile(david_user,date(1985,7,26),'Male',2,3,4,1)
    laura_profile = add_profile(laura_user,date(1988,8,26),'Male',2,3,1,3)
    leifos_profile = add_profile(leifos_user,date(1989,9,26),'Male',2,1,3,4)

    # Print out what we have added to the user
    for m in User.objects.all():
        print str(m)

    # populate gigs from songkick.com
    getSongkickGigs()
    gigs = Gig.objects.all()[:20]
    for u in UserProfile.objects.all():
        for gig in gigs:
            add_gig_attendance(gig, u)


# adds a band to the database or if they already exist
# returns the existing object
def add_band(name,image_Ref):
    if len(Band.objects.filter(name=name))>0:
        print 'band already populated'
        return Band.objects.get(name=name)

    b = Band.objects.get_or_create(name=name,image_Ref=image_Ref)[0]
    b.save()
    return b

# adds a user profile to the database or if they already exist
# returns the existing object
def add_profile(user, dob, gender, smokes, drinks, dances, involvement):
    # first check whether the user is already present,
    # if so return the existing object
    if len(UserProfile.objects.filter(user=user))>0:
        print 'profile already populated'
        return UserProfile.objects.get(user=user)
    u = UserProfile.objects.get_or_create(user=user, dob=dob, gender=gender,
            smokes=smokes, drinks=drinks,dances=dances,involvement=involvement)[0]
    u.save()
    return u

# adds a user to the database or if they already exist
# returns the existing object
def add_user(username,email,password):

    if len(User.objects.filter(username=username))>0:
        print 'user already populated'
        return User.objects.get(username=username)
    u = User.objects.create_user(username, email, password)
    u.save()
    return u

# adds a venue to the database or if they already exist
# returns the existing object
def add_venue(venue_id, name):
    if len(Venue.objects.filter(venue_id=venue_id))>0:
        print 'venue already populated'
        return Venue.objects.get(venue_id=venue_id)

    print "venue entered"
    v = Venue.objects.get_or_create(venue_id=venue_id, name=name)[0]
    v.save()
    print "added venue"
    return v

# adds a gig to the database or if they already exist
# returns the existing object
def add_gig(gig_id, date, time, city, venue, band):
    if len(Gig.objects.filter(gig_id=gig_id))>0:
        print 'gig already populated'
        return Gig.objects.get(gig_id=gig_id)

    print band,"gig entered"
    gig = Gig.objects.get_or_create(gig_id=gig_id, date=date, time=time, city=city, venue=venue, band=band)[0]
    gig.save()
    print "added gig"
    return gig

# adds a gig attendance to the database or if they already exist
# returns the existing object
def add_gig_attendance(gig, user):
    # check that the gig and user are not already present
    if len(GigAttendance.objects.filter(gig=gig,user=user))>0:
        print 'gig attendance already populated'
        return GigAttendance.objects.get(gig=gig,user=user)

    print "gig att entered"
    ga = GigAttendance.objects.get_or_create(gig=gig, user=user)[0]
    ga.save()
    print "added gig att"
    return ga

# New gig for populate db with songkick
def getSongkickGigs():

    # get images off song kick
    url_start = 'http://images.sk-static.com/images/media/profile_images/artists/'
    url_end = '/huge_avatar'

    print "loaded sk"
    for i in range(1,16):
        print i

        url = 'http://api.songkick.com/api/3.0/metro_areas/24473-uk-glasgow/calendar.json?apikey=jwzmbEyCAIwD7HCy&page=' + str(i) + '&per_page=50'
        try:
            jsonurl = urllib2.urlopen(url)
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
            pass
        sk = json.loads(jsonurl.read())

        for gig in sk['resultsPage']['results']['event']:
            
            # String for image for artist image
            artistID = 0 if len(gig['performance']) == 0 else gig['performance'][0]['artist']['id']
            artist_image = url_start + str(artistID) + url_end
            artist_name= '' if len(gig['performance']) == 0 else gig['performance'][0]['artist']['displayName']


            b = add_band(artist_name, artist_image)
            v = add_venue(0 if gig['venue']['id'] is None else gig['venue']['id'], gig['venue']['displayName'])
            time = '' if gig['start']['time'] is None else gig['start']['time']
            date = '' if gig['start']['date'] is None else gig['start']['date']
            g = add_gig(gig['id'], date, time, gig['location']['city'], v, b)

# Start execution here!
if __name__ == '__main__':
    print "Starting bandbuds model test script..."
    populate()