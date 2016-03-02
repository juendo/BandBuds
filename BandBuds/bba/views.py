from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from bba.models import Band, Gig, Venue, User_Profile
import datetime

def index(request):
    gigs = Gig.objects.all().order_by('date')
    # date of gigs for day
    context_dict = { 'gigs' : gigs }

    # Render the response and send it back!
    return render(request, 'bba/index.html', context_dict)

def calendar(request, month_string):
    month = datetime.datetime.strptime(month_string, "%Y-%m").month
    gigs = Gig.objects.all().filter(date__month=month)
    # date of gigs for day
    context_dict = { 'gigs' : gigs }

    # Render the response and send it back!
    return render(request, 'bba/index.html', context_dict)

def user(request,user_name_slug):
    try:
        user=User_Profile.objects.get(slug=user_name_slug)
        context_dict = {'user':user}

    except User_Profile.DoesNotExist:
        context_dict={}

    # Render the response and send it back!
    return render(request, 'bba/user.html', context_dict)