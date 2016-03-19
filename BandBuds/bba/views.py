from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from bba.models import Band, Gig, Venue, UserProfile, GigAttendance, User, Nudge
from datetime import date, datetime
from calendar import monthrange
from bba.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from sets import Set


print 'got here views'

def index(request):

    print 'got to index'

    gigs = Gig.objects.all().order_by('date')
    # date of gigs for day

    context_dict = { 'gigs' : gigs }
    # Render the response and send it back!
    return render(request, 'bba/index.html', context_dict)

# load the calendar page, including calendar for selecting a day from a month, and
# the list of gigs on today
def calendar(request):

    # get today's date
    today = date.today()

    # get all the gigs on today
    gigs = Gig.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)

    

    context_dict = { 
        'gigs' : gigs, 
        'month_string' : date.strftime(today, "%Y-%m"),
        'today' : today.day,
        'month' : create_calendar(today.year, today.month, today.day, 'f')
    }

    # Render the response and send it back!
    return render(request, 'bba/calendar.html', context_dict)

def create_calendar(year, month, day, with_buds):

    # get today's date
    today = date(year, month, day)
    # get gigs 
    if with_buds == 't':
        att = GigAttendance.objects.filter(gig__date__year=today.year, gig__date__month=today.month)
        gigs = Set()
        for a in att:
            gigs.add(a.gig)
    else:
        gigs = list(Gig.objects.filter(date__year=today.year, date__month=today.month))
    # get the first day of this month
    first_weekday = monthrange(today.year, today.month)[0]
    # get the length of this month
    month_length = monthrange(today.year, today.month)[1]
    # get the day of the month today
    current_day = today.day
    # create the 2D array representing the calendar cells (0 is empty, any other number is that day)
    calendar = []
    day_index = 1
    # for each row in the calendar
    for i in range(6):
        row = []
        # for each cell in the row
        for i in range(7):
            # if month hasn't started yet
            if day_index == 1:
                # if month starts on that day
                if first_weekday == i:
                    # if day is after current day
                    if day_index >= current_day:
                        # if there are gigs on that day
                        if len([gig for gig in gigs if gig.date.day == day_index]) > 0:
                            # show day
                            row.append(day_index)
                        else:
                            row.append(0)
                    else:
                        # otherwise day shouldn't appear
                        row.append(0)
                    # advance to next day
                    day_index += 1
                # if month hasn't started yet, day is blank
                else:
                    row.append(0)
            # if the month has started, and there are days left
            elif day_index <= month_length:
                # if day is after current day
                if day_index >= current_day:
                    if len([gig for gig in gigs if gig.date.day == day_index]) > 0:
                        # show day
                        row.append(day_index)
                    else:
                        row.append(0)
                else:
                    # otherwise day shouldn't appear
                    row.append(0)
                # advance to next day
                day_index += 1
            else:
                row.append(0)
        calendar.append(row)

    return calendar

# return json for reloading the calendar
def calendar_json(request, date_param, with_buds):

    params = date_param.split('-')    
    year = int(params[0])
    month = int(params[1])
    day = int(params[2])

    # check if date is the current month
    today = date.today()
    is_today = False

    if year == today.year and month == today.month:
        day = today.day
        is_today = True

    data = { 
        'calendar' : create_calendar(year, month, day, with_buds),
        'month_string' : str(year) + '-' + str(month).zfill(2),
        'day_string' : str(day),
        'prev_hidden' : is_today,
    }

    return JsonResponse(data)

# return the list of gigs on a given date
def gigs_on_date(request, date_param, with_buds):

    # extract the date fields
    date_param = date_param.split('-')
    # if getting only gigs which are being attended
    if with_buds == 't':
        # get all gig attendance objects for the date in question
        att = GigAttendance.objects.filter(gig__date__year=date_param[0], gig__date__month=date_param[1], gig__date__day=date_param[2])
        gigs = Set()
        # and extract their gigs
        for a in att:
            gigs.add(a.gig)
    # otherwise just get all the gigs on the given day
    else:
        gigs = Gig.objects.filter(date__year=date_param[0], date__month=date_param[1], date__day=date_param[2])

    return render(request, "bba/calendar/calendar_gig_list.html", { 'gigs' : gigs })

@login_required
def gig(request, gig_id):
    gig = Gig.objects.all().filter(gig_id=gig_id)[0]
    print gig
    print 'who is the user?'
    print request.user
    #profiles = UserProfile.objects.all()
    #for profile in profiles.iterator():
    #    ga = GigAttendance.objects.get_or_create(user=profile, gig=gig)[0]
    #    ga.save()

    userProf = UserProfile.objects.filter(user=request.user)[0]
    going = len(GigAttendance.objects.filter(user=userProf, gig=gig)) > 0

    nudges = Nudge.objects.filter(nudgee=userProf)
    
    buds = map(helper_get_user, GigAttendance.objects.filter(gig=gig))
    if going:
        notGoing = 'not-going-button'
    else:
        notGoing = ''
    context_dict = { 'gig' : gig , 'going' : going, 'buds' : buds, 'notGoingButton' : notGoing, 'nudges' : nudges }
    return render(request, 'bba/gig.html', context_dict)

@login_required
def bud_profile(request, budSlug):
    bud = UserProfile.objects.filter(slug=budSlug)[0]
    return render(request, 'bba/buds/bud_profile.html', { 'bud_to_show' : bud })

def helper_get_user(gig):
        return gig.user

def gig_bud(request, gig_id, bud_slug):
    gig = Gig.objects.all().filter(gig_id=gig_id)[0]
    buds = map(helper_get_user, GigAttendance.objects.filter(gig=gig))
    bud = UserProfile.objects.filter(slug=bud_slug)[0]
    context_dict = { 'bud_to_show' : bud, 'buds' : buds, 'gig' : gig }
    return render(request, 'bba/gig_buds.html', context_dict)

def user(request,user_name_slug):

    print 'got to user'

    try:
        user=UserProfile.objects.get(slug=user_name_slug)
        context_dict = {'user':user}

    except UserProfile.DoesNotExist:
        context_dict={}

    # Render the response and send it back!
    return render(request, 'bba/user/UserProfile.html', context_dict)

def add_profile(user):
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.save()
    return u

def register(request):
    context_dict ={}
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registering = True

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        print " is it valid?"

        # If the two forms are valid...
        if user_form.is_valid():

            print "yes valid"
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # create user profile object with default fields
            userProfile = add_profile(user)

            # logs in user
            userProfile.user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'],
                                )

            if userProfile.user.is_active:
               login(request, userProfile.user)

            print "hello!! " + str(userProfile.user.is_authenticated())


            return HttpResponseRedirect('../profile/'+userProfile.slug)

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors
            return render(request,'bba/index.html',{'user_form': user_form, 'errors': user_form.errors, 'registering': registering})

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        context_dict ={'user_form': user_form, 'registering': registering}

    print 'got to end: reg'
    # Render the template depending on the context.
    return render(request,'bba/index.html',context_dict)

def my_profile(request):
    userProf = UserProfile.objects.get(user=request.user)
    return profile(request, userProf.slug)

def profile(request, user_name_slug):

    slug_user = UserProfile.objects.get(slug=user_name_slug)

    print "hello!! " + str(slug_user.user.is_authenticated()), slug_user.user.username


    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        print '**************** is posted!!'

        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():
            user_profile = profile_form.save(commit=False)
            print '******************* is prof valid'

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'image' in request.FILES:
                user_profile.image = request.FILES['image']

                print '******************* about to save'
                user_profile.save()
            print "got to this user profile"
            registered = False

            return render(request,'bba/user/user_profile.html',{'slugUser':slug_user,'profile': user_profile, 'registered': registered})

        else:
            print profile_form.errors

    else:
        profile_form = UserProfileForm()

    bands = Band.objects.all().order_by('name')
    registered = True

    print 'got to end: prof'
    # Render the template depending on the context.
    return render(request,'bba/user/user_profile.html',{'slugUser':slug_user,'profile_form': profile_form, 'registered': registered, 'bands':bands})

def user_login(request):

    print 'got to user login'

    # Gather username and password
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Is the username and password valid
        user = authenticate(username=username, password=password)
        # If valid user
        if user:
            # has an activie account
           if user.is_active:
               login(request, user)
               return HttpResponseRedirect('../calendar')
           else:
               return HttpResponse("Your account for bandbuds has been disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Sorry bud! Invalid login details supplied.")
    else:
        return render(request, 'bba/index.html',{})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def im_going(request, gig_id):
    print "im_going"
    print gig_id
    try:
        gig = Gig.objects.filter(gig_id=gig_id)[0]
        print gig
        userProf = UserProfile.objects.filter(user=request.user)[0]
        print userProf
        # if user already going
        if len(GigAttendance.objects.filter(gig=gig, user=userProf)) > 0:
            print "going"
            ga = GigAttendance.objects.filter(gig=gig, user=userProf)[0]
            ga.delete()
            context_dict = { 'gig' : gig, 'notGoingButton' : 'not-going-button' }
        # if user not going
        else:
            print "not going"
            attend = GigAttendance.objects.get_or_create(gig=gig, user=userProf)[0]
            attend.save()
            context_dict = { 'going' : True, 'gig' : gig }
    except:
        context_dict = { 'gig' : gig }
    return render(request, 'bba/gig/gig_going_button.html', context_dict)



# for a user nuding another
@login_required
def nudge(request, user_slug, gig_id):
    nudgee = UserProfile.objects.get(slug=user_slug)
    nudger = request.user
    gig = Gig.objects.get(gig_id=gig_id)
    nudge = Nudge.objects.get_or_create(nudger=nudger, nudgee=nudgee, gig=gig)[0]
    nudge.save()
    return HttpResponse("Nudged")

@login_required
def like_band(request):

    print 'LIKING THIS!'
    band_id = None
    if request.method == 'GET':
        band_id = request.GET['band_id']
        user_id = request.GET['user_id']

        print '***band',band_id,'***user',user_id

    if band_id and user_id:

        user_profile=UserProfile.objects.get(slug=user_id)
        print 'gotta get'
        band = Band.objects.get(name=band_id)
        print 'gotta get thru this'
        add_liked_band(band,user_profile)
        print 'gotta go'


    return HttpResponse("")

# Like buttons helper function - to be refactored!!!
def add_liked_band(b,u):
    lb = LikedBand.objects.get_or_create(band=b,user=u)[0]
    print 'gotta go again',b,u,lb
    try:
        lb.save()
    except Exception as inst:
        print 'error'
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst

    print 'here?'
    return lb