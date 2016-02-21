import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BandBuds.settings')

from datetime import date

import django
django.setup()

from bba.models import Band, User, Liked_Band

def populate():
    bloc = add_band('Bloc Party', 'London', 'England', 1999, 'Indie')
    thewknd = add_band('The Weeknd','Toronto','Canada',1990,'R&B')

    stevo = add_user('0106105s','stevie','stando',date(1983,1,26),False,'Male','Jackie Daniels')

    bloc_like = add_liked_band(bloc, stevo)
    thewknd_like = add_liked_band(thewknd,stevo)

    # Print out what we have added to the user.
    for u in User.objects.all():
        for lb in Liked_Band.objects.all():
            print str(lb)

def add_band(name,city,country,formed,genre):
    b = Band.objects.get_or_create(name=name,city=city,country=country,formed=formed,genre=genre)[0]
    return b

def add_liked_band(b,u):
    lb = Liked_Band.objects.get_or_create(band=b,user=u)[0]
    return lb

def add_user(user_id, f_name,s_name, dob, smokes, gender, alcohol):
    u = User.objects.get_or_create(user_id=user_id, f_name=f_name,
                                    s_name=s_name, dob=dob, smokes=smokes, gender=gender, alcohol=alcohol)[0]
    u.save()
    return u

# Start execution here!
if __name__ == '__main__':
    print "Starting bandbuds model test script..."
    populate()