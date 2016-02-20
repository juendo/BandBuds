from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

def index(request):

    # Render the response and send it back!
    return render(request, 'bba/index.html')