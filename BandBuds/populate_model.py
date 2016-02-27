import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BandBuds.settings')

import json
import urllib
from datetime import date
from django.core.validators import validate_email

import django
django.setup()

from bba.models import Band, User, Liked_Band, Gig, Venue

API_KEY = "jwzmbEyCAIwD7HCy"

def populate():

    stevo = add_user('0106105s','stevie','stando',date(1983,1,26),False,'Male',True)

    bloc_like = add_liked_band(bloc, stevo)
    thewknd_like = add_liked_band(thewknd,stevo)

    # Print out what we have added to the user.
    for u in User.objects.all():
        for lb in Liked_Band.objects.all():
            print str(lb)

    getSongkickGigs()

def add_band(name,city,country,formed,genre):
    b = Band.objects.get_or_create(name=name,city=city,country=country,formed=formed,genre=genre)[0]
    return b

def add_liked_band(b,u):
    lb = Liked_Band.objects.get_or_create(band=b,user=u)[0]
    return lb

def add_user(user_id, f_Name,s_Name, dob, smokes, gender, drinks):
    u = User.objects.get_or_create(user_id=user_id, f_Name=f_Name,
                                    s_Name=s_Name, dob=dob, smokes=smokes, gender=gender, drinks=drinks)[0]
    u.save()
    return u
# New venue for populate db with songkick
def add_venue(venue_id, city, country, postcode, b_no, street):
    print "venue entered"
    v = Venue.objects.get_or_create(venue_id=venue_id, city=city, country=country, postcode=postcode, building_No=b_no, street=street)[0]
    v.save()
    print "added venue"
    return v

# New gig for populate db with songkick
def add_gig(date, time, city, venue, band):
    print "gig entered"
    gig = Gig.objects.get_or_create(date=date, time=time, city=city, venue=venue, band=band)[0]
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
    for gig in sk['resultsPage']['results']['event']:
        
        # String for image for artist image
        artistID = gig['performance'][0]['artist']['id']
        artist_image = url_start + artistID + url_end
        artist_name=gig['performance'][0]['artist']['displayName']
        print "next in loop " + artist_name

        b = add_band(artist_name, artist_image)
        v = add_venue(gig['venue']['id'], 'Glasgow', 'Scotland', 'G1 1AA', 1, 'Glasgow Street')
        time = '' if gig['start']['time'] is None else gig['start']['time']
        date = '' if gig['start']['date'] is None else gig['start']['date']
        g = add_gig(date, time, gig['location']['city'], v, b)

# Start execution here!
if __name__ == '__main__':
    print "Starting bandbuds model test script..."
    populate()