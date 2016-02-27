from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from bba.models import Band, Gig, Venue, User_Profile

def index(request):
    gigs = Gig.objects.all().order_by('date')
    # date of gigs for day
    context_dict = { 'gigs' : gigs }

    # Render the response and send it back!
    return render(request, 'bba/index.html', context_dict)

def user(request,user_name_slug):
    try:
        user_profile=User_Profile.objects.get(slug=user_name_slug)
        context_dict = {'user_name':user_profile.user}

    except User_Profile.DoesNotExist:
        context_dict={}

    # Render the response and send it back!
    return render(request, 'bba/index.html', context_dict)