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

    # extract date information
    requested_date = datetime.datetime.strptime(month_string, "%Y-%m")
    requested_month = requested_date.month
    requested_year = requested_date.year

    # get gigs for month
    gigs = Gig.objects.all().filter(date__month=requested_month).order_by('time')

    year = int(month_string.split('-')[0])

    # get next month details
    next_month = (int(month_string.split('-')[1]) % 12) + 1
    next_date = str(year if next_month != 1 else year + 1) + '-' + str(next_month).zfill(2)

    # get previous month details
    prev_month = ((int(month_string.split('-')[1]) + 10) % 12) + 1
    prev_date = str(year if prev_month != 12 else year - 1) + '-' + str(prev_month).zfill(2)

    day_string = "1"
    if requested_month == datetime.datetime.now().month:
        if requested_year == datetime.datetime.now().year:
            day_string = str(datetime.datetime.now().day)

    context_dict = { 'gigs' : gigs , 'next_date' : next_date, 'prev_date' : prev_date, 'month_string' : month_string, 'day_string' : day_string.zfill(2) }

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