from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from bba.models import Band, Gig, Venue, UserProfile, GigAttendance, User, Nudge, LikedBand,DisLikedBand, Buddy
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
        'month' : create_calendar(
                    today.year, 
                    today.month, 
                    today.day, 
                    list(Gig.objects.filter(date__year=today.year, date__month=today.month))
                )
    }

    # Render the response and send it back!
    return render(request, 'bba/calendar.html', context_dict)

def create_calendar(year, month, day, gigs):

    # get today's date
    today = date(year, month, day)
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

    search = request.GET['search']

    # if getting only gigs which are being attended
    if with_buds == 't':
        # get gig attendances for given month
        att = GigAttendance.objects.filter(
                gig__date__year=year,
                gig__date__month=month
            ) | \
            GigAttendance.objects.filter(
                gig__date__year=year, 
                gig__date__month=month
            )
            # filter on search term if necessary
        if search != '':
            att = att.filter(
                    gig__band__name=search
                ) | \
                att.filter(
                    gig__venue__name=search
                )
        gigs = Set()
        # and extract the gigs
        for a in att:
            gigs.add(a.gig)
    # otherwise just get all the gigs on the given day
    else:
        gigs = Gig.objects.filter(
                date__year=year, 
                date__month=month, 
            ) | \
            Gig.objects.filter(
                date__year=year,
                date__month=month,
            )
        if search != '':
            gigs = gigs.filter(
                    band__name=search
                ) | \
                gigs.filter(
                    venue__name=search
                )

    cal = create_calendar(year, month, day, gigs)

    data = { 
        'calendar' : cal,
        'month_string' : str(year) + '-' + str(month).zfill(2),
        'day_string' : str(next((x for i, x in enumerate(sum(cal, [])) if x != 0), 'No Gigs!')),
        'prev_hidden' : is_today,
    }

    return JsonResponse(data)

# return the list of gigs on a given date
def gigs_on_date(request, date_param, with_buds):

    # extract the date fields
    date_param = date_param.split('-')

    # get the search text
    search = request.GET['search']

    # if getting only gigs which are being attended
    if with_buds == 't':
        # get gig attendances for given month
        att = GigAttendance.objects.filter(
                gig__date__year=date_param[0], 
                gig__date__month=date_param[1], 
                gig__date__day=date_param[2],
            ) | \
            GigAttendance.objects.filter(
                gig__date__year=date_param[0], 
                gig__date__month=date_param[1], 
                gig__date__day=date_param[2],
            )
            # filter on search term if necessary
        if search != '':
            att = att.filter(
                    gig__band__name=search
                ) | \
                att.filter(
                    gig__venue__name=search
                )
        gigs = Set()
        # and extract the gigs
        for a in att:
            gigs.add(a.gig)
    # otherwise just get all the gigs on the given day
    else:
        gigs = Gig.objects.filter(
                date__year=date_param[0], 
                date__month=date_param[1], 
                date__day=date_param[2],
            ) | \
            Gig.objects.filter(
                date__year=date_param[0],
                date__month=date_param[1],
                date__day=date_param[2],
            )
        if search != '':
            gigs = gigs.filter(
                    band__name=search
                ) | \
                gigs.filter(
                    venue__name=search
                )

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
def bud_profile(request, bud_slug):

    bud = UserProfile.objects.get(slug=bud_slug)
    #user = request.user

    #nudge = Buddy.objects.get_or_create(user=user, bud=bud, gig=gig)[0]
    #nudge.save()


    return render(request, 'bba/buds/bud_profile.html', { 'bud' : bud})

def helper_get_user(gig):
        return gig.user

# highlights given bud in context of bud_slug relating to gig gig_id
# displays other buds attending as well
def gig_bud(request, gig_id, bud_slug):


    #    gig = Gig.objects.all().filter(gig_id=gig_id)[0]
    gig = Gig.objects.get(gig_id=gig_id)
    buds = map(helper_get_user, GigAttendance.objects.filter(gig=gig))
    bud_to_show = UserProfile.objects.get(slug=bud_slug)


    # user = UserProfile.objects.get(username=username)
    #    user_profile = UserProfile.objects.get(user=user)

    # check to see if nudge button clicked via ajax button
  #  if request.method == 'GET':

 #       nudge = Buddy.objects.get_or_create(user=userProfile, bud=bud_to_show, gig=gig)[0]
    #        nudge.save()

    context_dict = { 'bud_to_show' : bud_to_show, 'buds' : buds, 'gig' : gig}

    return render(request, 'bba/gig_buds.html', context_dict)


def user(request,user_name_slug):

    print 'got to user'

    try:
        user_profile=UserProfile.objects.get(slug=user_name_slug)
        context_dict = {'user_profile':user_profile}

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
            user_profile = add_profile(user)

            # logs in user
            user_profile.user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'],
                                )

            if user_profile.user.is_active:
               login(request, user_profile.user)

            print "hello!! " + str(user_profile.user.is_authenticated())


            return HttpResponseRedirect('../profile/'+user_profile.slug)

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors
            return render(request,'bba/index.html',{'user_form': user_form, 'errors': user_form.errors})

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

    user_profile = UserProfile.objects.get(slug=user_name_slug)

    print user_profile.drinks,''

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':


        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():
            user_data = profile_form.save(commit=False)
            print '******************* is prof valid'

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'image' in request.FILES:
                user_data.image = request.FILES['image']

                print '****************** about to save'


            print "got to this user profile"


            registered = True
            user_profile.drinks=user_data.drinks
            user_profile.save()



        else:
            print profile_form.errors

    else:
        profile_form = UserProfileForm()


    # data for liked bands of a user
    liked_bands=LikedBand.objects.filter(user=user_profile)
    prefSet=[]
    for i in range(len(liked_bands)):
        prefSet.append(liked_bands[i].band)
    bands=Band.objects.all()
    newbies=list(set(bands)-set(prefSet))

    # data for disliked bands of a user
    disliked_bands=DisLikedBand.objects.filter(user=user_profile)
    prefSet=[]
    for i in range(len(disliked_bands)):
        prefSet.append(disliked_bands[i].band)
    bands=Band.objects.all()
    newbies=list(set(bands)-set(prefSet))

    # data for buddy request notifications
    nudge=Buddy.objects.filter(buddy=user_profile)
    nudgeList=[]
    print "******** nudging"
    for i in range(len(nudge)):
        if nudge[i].accept==False:
            nudgeList.append(nudge[i])
    for i in range(len(nudgeList)):
        print nudgeList[i].user

    registered = True


    context_dict={'user_profile':user_profile,'profile_form': profile_form, 'registered': registered, 'bands':newbies[:10],'liked_bands':liked_bands[:5],'disliked_bands':disliked_bands[:5],'nudges':nudgeList[:5]}

    # Render the template depending on the context
    return render(request,'bba/user/user_profile.html',context_dict)




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



# for a user nudging another
@login_required
def nudge(request):

    if request.method == 'GET':

        print 'nudging..'

        user_id = request.GET['user_id']
        bud_id = request.GET['bud_id']
        gig_id = request.GET['gig_id']

        try:
            user=User.objects.get(username=user_id)
            user_profile=UserProfile.objects.get(user=user)

            bud_profile=UserProfile.objects.get(slug=bud_id)

            gig = Gig.objects.get(gig_id=gig_id)

        except Exception as exp:
            print exp
            return HttpResponse("Error")

        print 'saving..'

        add_buddy_request(user_profile,bud_profile,gig)

        print 'saved.'


    return HttpResponse("Nudged")
#    return render("Nudged", 'bba/bud/bud_profile.html', context_dict)

@login_required
def like_band(request):

    band_id = None
    if request.method == 'GET':

        band_id = request.GET['band_id']
        user_id = request.GET['user_id']

        user=User.objects.get(username=user_id)
        user_profile=UserProfile.objects.get(user=user)

        band = Band.objects.get(name=band_id)
        add_liked_band(band,user_profile)


    return HttpResponse("")

# Like buttons helper function - to be refactored!!!
def add_liked_band(b,u):
    lb = LikedBand.objects.get_or_create(band=b,user=u)[0]
    print 'gotta go again',b,u,lb
    try:
        lb.save()
    except :
        print 'error'

    print 'here?'
    return lb



@login_required
def dislike_band(request):
    band_id = None
    if request.method == 'GET':

        band_id = request.GET['band_id']
        user_id = request.GET['user_id']

        user=User.objects.get(username=user_id)
        user_profile=UserProfile.objects.get(user=user)
        band = Band.objects.get(name=band_id)

        add_disliked_band(band,user_profile)

    print 'disliked band!!!!'
    return HttpResponse("")

# Like buttons helper function - to be refactored!!!
def add_liked_band(b,u):
    lb = LikedBand.objects.get_or_create(band=b,user=u)[0]
    try:
        lb.save()
    except :
        print 'error'

    return lb

# Like buttons helper function - to be refactored!!!
def add_disliked_band(b,u):
    print 'step 4!!'

    dlb = DisLikedBand.objects.get_or_create(band=b,user=u)[0]
    try:
        dlb.save()
    except :
        print 'error'
    print 'step 5!!'
    return dlb

# helper function - to be refactored!!!
def add_buddy_request(user,buddy,gig):
    try:
        bud_req = Buddy.objects.get_or_create(user=user,buddy=buddy,gig=gig)
        bud_req.save()
    except Exception as exp:
        print 'error'
        print exp

    return bud_req