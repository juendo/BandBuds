from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from bba.models import Band, Gig, Venue, UserProfile, GigAttendance, User, LikedBand,DisLikedBand, Buddy
from datetime import date, datetime
from calendar import monthrange
from bba.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from sets import Set
import random

# descriptions of gig attributes for each possible integer value
DANCE = {0:"Toe-tapper", 1:"Shoulder shuffler", 2:"Hip shaker", 3:"Arms waver", 4:"Gets down"}
DRINK = {0:"Teetotal", 1:"Social drinker", 2:"Drinks loads", 3:"Drinks too much", 4:"Has a drink problem"}
INVOLVE = {0:"Stands at the bar", 1:"Stays at the back", 2:"Next to stage", 3:"Crowd surfer", 4:"In the mosh pit"}
SMOKE = {0:"Non-smoker", 1:"Occasional smoker", 2:"Social smoker", 3:"Regular smoker", 4:"Smokes like a chimney"}

SMOKE_IMGS = {0:"bb_smoke_not", 1:"bb_smoke_chimney", 2:"bb_smoke_social", 3:"bb_smoke_regular", 4:"bb_smoke_chimney"}
DRINK_IMGS = {0:"bb_drinks_teetotal", 1:"bb_drinks_social", 2:"bb_drinks_loads", 3:"bb_drinks_too_much", 4:"bb_drinks_i_have_a_problem"}
INVOLVE_IMGS = {0:"bb_involvement_bar", 1:"bb_involvement_back", 2:"bb_involvement_crowd", 3:"bb_involvement_stage", 4:"bb_involvement_pit"}
DANCE_IMGS = {0:"bb_dance_toe_tap", 1:"bb_dance_shoulder_shuffle", 2:"bb_dance_hip_shaker", 3:"bb_dance_arms_waving", 4:"bb_dance_get_down"}
# load the home page
def index(request):

    return render(request, 'bba/index.html', {})

# load the calendar page, this includes:
# a calendar for selecting a day and a month
# a list of the gigs on that day
def calendar(request):

    # get today's date
    today = date.today()

    # get all the gigs on today
    gigs = Gig.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)

    # pass this data the template
    context_dict = {
        'gigs' : gigs,
        'month_string' : date.strftime(today, "%Y-%m"),
        'today' : today.day,
        # this is a 2D array explaining to the template how to load the calendar cells
        'month' : create_calendar(
                    today.year, 
                    today.month, 
                    today.day, 
                    list(Gig.objects.filter(date__year=today.year, date__month=today.month))
                )
    }
    return render(request, 'bba/calendar.html', context_dict)

# helper function to create 2D array to describe the cells in the calendar
# eg [[0,0,0,1,2,3,4], [5,6,7,8,9,10,11],...] etc
# accepts a list of gigs, so that days with no gigs on that list can be blanked from the calendar
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

# return json so that calendar cells may be reloaded to adjust to
# search or filter parameters
def calendar_json(request, date_param, with_buds):

    # extract the date info from the url
    params = date_param.split('-')
    year = int(params[0])
    month = int(params[1])
    day = int(params[2])

    # check if the requested date falls in the current month
    today = date.today()
    is_today = False
    if year == today.year and month == today.month:
        day = today.day
        is_today = True

    # get the search parameter, if any
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
        # and extract the unique gigs (each may have more than one atendance)
        for a in att:
            gigs.add(a.gig)
    # if not filtering on attended gigs, just get all the gigs on the given day
    else:
        gigs = Gig.objects.filter(
                date__year=year, 
                date__month=month, 
            ) | \
            Gig.objects.filter(
                date__year=year,
                date__month=month,
            )
        # and possibly filter by the search parameter
        if search != '':
            gigs = gigs.filter(
                    band__name=search
                ) | \
                gigs.filter(
                    venue__name=search
                )

    # create 2D calendar array for the given date, and list of gigs
    cal = create_calendar(year, month, day, gigs)

    data = { 
        'calendar' : cal,
        'month_string' : str(year) + '-' + str(month).zfill(2),
        # day string is first day with gigs, if any, otherwise just No Gigs!
        'day_string' : str(next((x for i, x in enumerate(sum(cal, [])) if x != 0), 'No Gigs!')),
        'prev_hidden' : is_today,
    }
    # return the json
    return JsonResponse(data)

# return the calendar gig list template, complete with gigs
# matching the request (used in ajax request)
# similar to calendar_json, but for loading the gigs into the view
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

# load the gig page for gig with given id
# by this point the user must be logged in
@login_required
def gig(request, gig_id):

    # get the requested gig
    gig = Gig.objects.all().filter(gig_id=gig_id)[0]

    # get the logged in user's profile
    userProf = UserProfile.objects.filter(user=request.user)[0]

    # check if the user is attending this gig
    going = len(GigAttendance.objects.filter(user=userProf, gig=gig)) > 0

    # helper function to get user from GigAttendance object
    def helper_get_user(gigAtt):
        return gigAtt.user

    # get the profiles of the users who are attending this gig (excluding current user)
    buds = map(helper_get_user, GigAttendance.objects.filter(gig=gig).exclude(user=userProf))

    # if user is going, pass parameter to alter css of the I'm Going button so that it appears green
    if going:
        notGoing = 'not-going-button'
    else:
        notGoing = ''

    # render the template
    context_dict = { 'gig' : gig , 'going' : going, 'buds' : buds, 'notGoingButton' : notGoing }
    return render(request, 'bba/gig.html', context_dict)

# view a potntial bud's profile in the context of a specific gig:
# i.e. the other buds going to that gig are shown in the list
def gig_bud(request, gig_id, bud_slug):

    # get the current user's profile
    currentUser = UserProfile.objects.filter(user=request.user)[0]

    # get the gig
    gig = Gig.objects.get(gig_id=gig_id)

    # helper function to get user from GigAttendance object
    def helper_get_user(gigAtt):
        return gigAtt.user

    # get the bud to view
    bud = UserProfile.objects.get(slug=bud_slug)

    # get the buds (not including the current user or the bud being viewed)
    buds = map(helper_get_user, GigAttendance.objects.filter(gig=gig).exclude(user=currentUser).exclude(user=bud))

    # check if the user has already nudged this person
    nudged = len(Buddy.objects.filter(user=currentUser, buddy=bud, gig=gig)) > 0

    # get the potential bud's likes and dislikes
    liked_bands = LikedBand.objects.filter(user=bud)[:15]
    disliked_bands = DisLikedBand.objects.filter(user=bud)[:15]

    # render template
    context_dict = { 
        'bud_to_show' : bud, 
        'buds' : buds, 
        'gig' : gig, 
        'smokes' : SMOKE[bud.smokes], 
        'dances' : DANCE[bud.dances], 
        'drinks' : DRINK[bud.drinks], 
        'involvement' : INVOLVE[bud.involvement],
        'smokes_img' : SMOKE_IMGS[bud.smokes], 
        'dances_img' : DANCE_IMGS[bud.dances], 
        'drinks_img' : DRINK_IMGS[bud.drinks], 
        'involvement_img' : INVOLVE_IMGS[bud.involvement],
        'nudged' : nudged,
        'liked_bands' : liked_bands,
        'disliked_bands' : disliked_bands,
        'profile' : False
    }

    return render(request, 'bba/gig_buds.html', context_dict)

# register a user
def register(request):
    context_dict = {}
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registering = True

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():

            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # create user profile object with default fields
            user_profile = UserProfile.objects.get_or_create(user=user)[0]

            # logs in user
            user_profile.user = authenticate(
                                    username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'],
                                )
            user_profile.save()

            if user_profile.user.is_active:
               login(request, user_profile.user)

            return HttpResponseRedirect('../edit-profile/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            return render(request,'bba/index.html',{'user_form': user_form, 'errors': user_form.errors})

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        context_dict ={'user_form': user_form, 'registering': registering}

    print 'got to end: reg'
    # Render the template depending on the context.
    return render(request,'bba/index.html',context_dict)

# show the current user their profile
@login_required
def my_profile(request):

    # get the user's profile
    profile = UserProfile.objects.get(user=request.user)

    liked_bands = LikedBand.objects.filter(user=profile)[:15]
    nudges = Buddy.objects.filter(buddy=profile, accept=False)

    accepted = Buddy.objects.filter(user=profile, accept=True)

    # data for disliked bands of a user
    disliked_bands = DisLikedBand.objects.filter(user=profile)[:15]

    context_dict = { 
        'bud_to_show' : profile, 
        'gig' : gig, 
        'smokes' : SMOKE[profile.smokes], 
        'dances' : DANCE[profile.dances], 
        'drinks' : DRINK[profile.drinks], 
        'involvement' : INVOLVE[profile.involvement], 
        'smokes_img' : SMOKE_IMGS[profile.smokes], 
        'dances_img' : DANCE_IMGS[profile.dances], 
        'drinks_img' : DRINK_IMGS[profile.drinks], 
        'involvement_img' : INVOLVE_IMGS[profile.involvement],
        'liked_bands' : liked_bands,
        'disliked_bands' : disliked_bands,
        'nudges' : nudges,
        'accepted' : accepted,
        'profile' : True,
    }

    return render(request, 'bba/user/my_profile.html', context_dict)

# allow a user to edit their profile
@login_required
def edit_profile(request):

    # get the user's profile
    profile = UserProfile.objects.get(user=request.user)

    # if they have submitted profile data
    if request.method == 'POST':

        profile_form = UserProfileForm(data=request.POST)
        # validate it
        if profile_form.is_valid():
            profile.dob = profile_form.cleaned_data['dob']
            profile.gender = profile_form.cleaned_data['gender']
            profile.smokes = profile_form.cleaned_data['smokes']
            profile.drinks = profile_form.cleaned_data['drinks']
            profile.dances = profile_form.cleaned_data['dances']
            profile.involvement = profile_form.cleaned_data['involvement']

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'image' in request.FILES:
                profile.image = request.FILES['image']

            # save and show take the user to their profile
            registered = True
            profile.user = request.user
            profile.save()

            return HttpResponseRedirect('/profile/')

    registered = True

    context_dict = {
        'user_profile':profile,
        'profile_form': UserProfileForm(), 
        'registered': registered, 
        'bands':new_bands(profile)[:10],
    }

    # Render the template depending on the context
    return render(request,'bba/user/user_profile.html',context_dict)

# login a user
def user_login(request):
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

               return HttpResponseRedirect('/calendar/')
           else:
               return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return render(request, 'bba/index.html',{})

# logout the user
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# either indicate that a user is attending a gig, 
# or that they no longer are attending
# this is called as an ajax request
@login_required
def im_going(request, gig_id):
    
    try:
        # get the gig and user in question
        gig = Gig.objects.filter(gig_id=gig_id)[0]

        userProf = UserProfile.objects.filter(user=request.user)[0]

        # if user already going
        if len(GigAttendance.objects.filter(gig=gig, user=userProf)) > 0:

            ga = GigAttendance.objects.filter(gig=gig, user=userProf)[0]

            # delete the attendance object
            ga.delete()
            context_dict = { 'gig' : gig, 'notGoingButton' : 'not-going-button' }
        # if user not going
        else:
            # create attendance object
            attend = GigAttendance.objects.get_or_create(gig=gig, user=userProf)[0]
            attend.save()
            context_dict = { 'going' : True, 'gig' : gig }
    except:
        context_dict = { 'gig' : gig }

    # return the new button to show
    return HttpResponse('Going')

# allow a user to nudge another user
# this is an ajax reqest
@login_required
def nudge(request):

    # get the details of the nudge request
    if request.method == 'GET':
        bud_id = request.GET['bud_id']
        gig_id = request.GET['gig_id']
        user = request.user

        userProf = UserProfile.objects.filter(user=user)[0]
        budProf = UserProfile.objects.get(slug=bud_id)
        gig = Gig.objects.get(gig_id=gig_id)

        # if already nudged
        if len(Buddy.objects.filter(gig=gig, user=userProf, buddy=budProf)) > 0:

            b = Buddy.objects.filter(gig=gig, user=userProf, buddy=budProf)[0]
            # remove the nudge
            b.delete()
            context_dict = { 'nudged' : False }
        # if not yet nudged
        else:
            # save the nudge
            b = Buddy.objects.get_or_create(gig=gig, user=userProf, buddy=budProf)[0]
            b.save()
            context_dict = { 'nudged' : True }

        # return the new nudge button
        return render(request, 'bba/buds/bud_nudge_button.html', context_dict)

# indicate that a user likes a given band
@login_required
def like_band(request):

    band_id = None
    if request.method == 'GET':

        # get the details
        band_id = request.GET['band_id']
        user_id = request.GET['user_id']

        user = User.objects.get(username=user_id)
        user_profile = UserProfile.objects.get(user=user)

        # create the liked band object
        band = Band.objects.get(name=band_id)
        lb = LikedBand.objects.get_or_create(band=band, user=user_profile)[0]
        try:
            lb.save()
        except :
            pass
    return render(request, 'bba/user/band_like_box.html', { 'band' : random.choice(new_bands(user_profile)), 'user_profile' : user_profile })

# indicate the a user dislikes a given band
@login_required
def dislike_band(request):
    band_id = None
    if request.method == 'GET':

        band_id = request.GET['band_id']
        user_id = request.GET['user_id']

        user = User.objects.get(username=user_id)
        user_profile = UserProfile.objects.get(user=user)
        band = Band.objects.get(name=band_id)

        # create the disliked band object
        band = Band.objects.get(name=band_id)
        dlb = DisLikedBand.objects.get_or_create(band=band, user=user_profile)[0]
        try:
            dlb.save()
        except :
            pass
    return render(request, 'bba/user/band_like_box.html', { 'band' : random.choice(new_bands(user_profile)), 'user_profile' : user_profile })

# get some new bands for a user to like or dislike
def new_bands(profile):
    # get their liked bands
    liked_bands = LikedBand.objects.filter(user=profile)
    lb = []
    for l in liked_bands:
        lb.append(l.band)

    # and disliked bands
    disliked_bands = DisLikedBand.objects.filter(user=profile)
    db = []
    for d in disliked_bands:
        db.append(d.band)

    # return those bands yet to be liked or disliked
    return list(set(Band.objects.all()) - set(lb) - set(db))

# accept a nudge
def accept(request):
    if request.method == 'GET':
        gig_id = request.GET['gigid']
        budslug = request.GET['bud']
        gig = Gig.objects.filter(gig_id=gig_id)[0]
        bud = UserProfile.objects.filter(slug=budslug)
        userProfile = UserProfile.objects.filter(user=request.user)[0]
        nudge = Buddy.objects.filter(gig=gig, user=bud, buddy=userProfile)[0]
        nudge.accept = True
        nudge.save()
    return HttpResponse('')

# accept a nudge
def decline(request):
    if request.method == 'GET':
        gig_id = request.GET['gigid']
        budslug = request.GET['bud']
        gig = Gig.objects.filter(gig_id=gig_id)[0]
        bud = UserProfile.objects.filter(slug=budslug)
        userProfile = UserProfile.objects.filter(user=request.user)[0]
        nudge = Buddy.objects.filter(gig=gig, user=bud, buddy=userProfile)[0]
        nudge.delete()
    return HttpResponse('')


