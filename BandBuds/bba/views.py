from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from bba.models import Band, Gig, Venue, UserProfile, GigAttendance
import datetime
from bba.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required

print 'got here views'

def index(request):

    print 'got to index'

    gigs = Gig.objects.all().order_by('date')
    # date of gigs for day
    context_dict = { 'gigs' : gigs }

    # Render the response and send it back!
    return render(request, 'bba/index.html', context_dict)

def calendar(request):

    print 'got to calendar'

    # get gigs for month
    gigs = Gig.objects.all().filter(date__month=datetime.datetime.now().month, date__day=datetime.datetime.now().day)

    context_dict = { 
        'gigs' : gigs, 
        'month_string' : datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m"), 
        'day_string' : datetime.datetime.now().day 
    }

    # Render the response and send it back!
    return render(request, 'bba/calendar.html', context_dict)

# return the list of gigs on a given date
def gigs_on_date(request, query):
    query = query.split('-')
    # get gigs on date
    gigs = Gig.objects.filter(date__year=query[0], date__month=query[1], date__day=query[2])
    context = {
      'gigs' : gigs,
    }
    return render(request, "bba/calendar/calendar_gig_list.html", context)

def gig(request, gig_id):
    gig = Gig.objects.all().filter(gig_id=gig_id)[0]
    print gig
    profiles = UserProfile.objects.all()
    for profile in profiles.iterator():
        ga = GigAttendance.objects.get_or_create(user=profile, gig=gig)[0]
        ga.save()

    going = len(GigAttendance.objects.filter(user=UserProfile.objects.all()[0], gig=gig)) > 0
    
    buds = map(helper_get_user, GigAttendance.objects.filter(gig=gig))
    context_dict = { 'gig' : gig , 'going' : going, 'buds' : buds }
    return render(request, 'bba/gig.html', context_dict)

def helper_get_user(gig):
        return gig.user

def gig_bud(request, gig_id, bud_slug):
    gig = Gig.objects.all().filter(gig_id=gig_id)[0]
    buds = map(helper_get_user, GigAttendance.objects.filter(gig=gig))
    bud = UserProfile.objects.filter(slug=bud_slug)[0]
    context_dict = { 'bud_to_show' : bud, 'buds' : buds, 'gig' : gig }
    return render(request, 'bba/gig.html', context_dict)

def user(request,user_name_slug):

    print 'got to user'

    try:
        user=UserProfile.objects.get(slug=user_name_slug)
        context_dict = {'user':user}

    except UserProfile.DoesNotExist:
        context_dict={}

    # Render the response and send it back!
    return render(request, 'bba/user/UserProfile.html', context_dict)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'image' in request.FILES:
                profile.image = request.FILES['image']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    print 'got to end'
    # Render the template depending on the context.
    return render(request,'bba/user/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

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
def like_band(request):

    band_id = None
    if request.method == 'GET':
        band_id = request.GET['band_id']

    likes = 0
    if band_id:
        band = Category.objects.get(id=int(band_id))
        if band:
            likes = band.likes + 1
            band.likes =  likes
            band.save()

    return HttpResponse(likes)