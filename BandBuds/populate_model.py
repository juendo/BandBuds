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

    # Creating mock users
    stevo_user = add_user('steve','e@m.ail','sesame')
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
    stevo_profile = add_profile(stevo_user,date(1983,1,26),'Male',0,0,0,0)
    lewis_profile = add_profile(lewis_user,date(1990,1,14),'Male',0,0,1,1)
    anaJ_profile = add_profile(anaJ_user,date(1950,2,26),'Male',0,1,1,0)
    gladis_profile = add_profile(gladis_user,date(1950,2,26),'Female',1,1,0,0)
    joel_profile = add_profile(joel_user,date(1993,1,15),'Male',0,0,0,0)
    rob_profile = add_profile(rob_user,date(1993,1,20),'Male',0,0,0,0)
    mario_profile = add_profile(mario_user,date(1984,3,26),'Male',0,0,0,0)
    polly_profile = add_profile(polly_user,date(1982,5,26),'Female',0,0,0,0)
    david_profile = add_profile(david_user,date(1985,7,26),'Male',0,0,0,0)
    laura_profile = add_profile(laura_user,date(1988,8,26),'Male',0,0,0,0)
    leifos_profile = add_profile(leifos_user,date(1989,9,26),'Male',0,0,0,0)

    # Print out what we have added to the user
    for m in User.objects.all():
        print str(m)

    # populate gigs from songkick.com
    getSongkickGigs()
    gigs = Gig.objects.all()[:20]
    for u in UserProfile.objects.all():
        for gig in gigs:
            add_gig_attendance(gig, u)


def add_band(name,image_Ref):
    b = Band.objects.get_or_create(name=name,image_Ref=image_Ref)[0]
    b.save()
    return b

def add_profile(user, dob, gender, smokes, drinks, dances, involvement):
    u = UserProfile.objects.get_or_create(user=user, dob=dob, gender=gender,
            smokes=smokes, drinks=drinks,dances=dances,involvement=involvement)[0]
    u.save()
    return u

def add_user(username,email,password):
    u = User.objects.create_user(username, email, password)
    u.save()
    return u

# New venue for populate db with songkick
def add_venue(venue_id, name):
    print "venue entered"
    v = Venue.objects.get_or_create(venue_id=venue_id, name=name)[0]
    v.save()
    print "added venue"
    return v

# New gig for populate db with songkick
def add_gig(gig_id, date, time, city, venue, band):
    print "gig entered"
    gig = Gig.objects.get_or_create(gig_id=gig_id, date=date, time=time, city=city, venue=venue, band=band)[0]
    gig.save()
    print "added gig"
    return gig

def add_gig_attendance(gig, user):
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