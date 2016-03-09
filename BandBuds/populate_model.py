import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BandBuds.settings')

import json
import urllib
from datetime import date
from django.core.validators import validate_email
import django
django.setup()
from django.core.validators import validate_email

from bba.models import Band, UserProfile, LikedBand, Gig, Venue

from django.contrib.auth.models import User

API_KEY = "jwzmbEyCAIwD7HCy"

def populate():

    # Creating mock users
    stevo_user = add_user('steve','e@m.ail','sesame')
    anaJ_user = add_user('Ana Jahnke','ana_jahnke@hotmail.com','123')
    lewis_user = add_user('Lewis','l@hotmail.com','123')
    gladis_user = add_user('Gladis','glad@hotmail.com','123')
    franis_user = add_user('Francis','fran@hotmail.com','123')
    lue_user = add_user('Lue Wang','lu@hotmail.com','123')
    mario_user = add_user('Mario','mario@hotmail.com','123')
    polly_user = add_user('Polly','poll@hotmail.com','123')
    abdul_user = add_user('Abdul','abd@hotmail.com','123')
    tugce_user = add_user('Tugce','tg@hotmail.com','123')
    boramas_user = add_user('Boramas','bor@hotmail.com','123')

    # Create profile
    stevo_profile = add_profile(stevo_user,date(1983,1,26),False,'Male', True)
    lewis_profile = add_profile(lewis_user,date(1990,1,14),False,'Male', True)
    anaJ_profile = add_profile(anaJ_user,date(1950,2,26),False,'Female', True)
    gladis_profile = add_profile(gladis_user,date(1950,2,26),False,'Female', True)
    franis_profile = add_profile(franis_user,date(1993,1,15),False,'Female', True)
    lue_profile = add_profile(lue_user,date(1993,1,20),False,'Female', True)
    mario_profile = add_profile(mario_user,date(1984,3,26),False,'Male', True)
    polly_profile = add_profile(polly_user,date(1982,5,26),False,'Female', True)
    abdul_profile = add_profile(abdul_user,date(1985,7,26),False,'Male', True)
    tugce_profile = add_profile(tugce_user,date(1988,8,26),False,'Female', True)
    boramas_profile = add_profile(boramas_user,date(1989,9,26),False,'Male', True)

    # Print out what we have added to the user
    for m in User.objects.all():
            print str(m)

    # populate gigs from songkick.com
    getSongkickGigs()


def add_band(name,image_Ref):
    b = Band.objects.get_or_create(name=name,image_Ref=image_Ref)[0]
    return b

def add_LikedBand(b,u):
    lb = LikedBand.objects.get_or_create(band=b,user=u)[0]
    return lb

def add_profile(user, dob, smokes, gender, drinks):
    u = UserProfile.objects.get_or_create(user=user, dob=dob, smokes=smokes, gender=gender, drinks=drinks)[0]
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


# New gig for populate db with songkick
def getSongkickGigs():
    url = 'http://api.songkick.com/api/3.0/metro_areas/24473-uk-glasgow/calendar.json?apikey=jwzmbEyCAIwD7HCy&page=1&per_page=50'
    jsonurl = urllib.urlopen(url)
    sk = json.loads(jsonurl.read())

    # get images off song kick
    url_start = 'http://images.sk-static.com/images/media/profile_images/artists/'
    url_end = '/huge_avatar'

    print "loaded sk"
    for i in range(1,11):

        url = 'http://api.songkick.com/api/3.0/metro_areas/24473-uk-glasgow/calendar.json?apikey=jwzmbEyCAIwD7HCy&page=' + str(i) + '&per_page=50'
        jsonurl = urllib.urlopen(url)
        sk = json.loads(jsonurl.read())

        # get images off song kick
        url_start = 'http://images.sk-static.com/images/media/profile_images/artists/'
        url_end = '/huge_avatar'

        for gig in sk['resultsPage']['results']['event']:
            
            # String for image for artist image
            artistID = 0 if len(gig['performance']) == 0 else gig['performance'][0]['artist']['id']
            artist_image = url_start + str(artistID) + url_end
            artist_name= '' if len(gig['performance']) == 0 else gig['performance'][0]['artist']['displayName']
            print "next in loop " + artist_name

            b = add_band(artist_name, artist_image)
            v = add_venue(0 if gig['venue']['id'] is None else gig['venue']['id'], gig['venue']['displayName'])
            time = '' if gig['start']['time'] is None else gig['start']['time']
            date = '' if gig['start']['date'] is None else gig['start']['date']
            g = add_gig(gig['id'], date, time, gig['location']['city'], v, b)

# Start execution here!
if __name__ == '__main__':
    print "Starting bandbuds model test script..."
    populate()