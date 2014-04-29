from django.shortcuts import render

# from django.core.context_processors import csrf

# Create your views here.
from django import forms
from django.template import RequestContext

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.utils import timezone
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

def login(request) :

    return render_to_response('login.html',
            context_instance=RequestContext(request))

def auth_view(request) :

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username = username, password = password)

    if user is not None :
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else :
        return HttpResponseRedirect('/accounts/invalid')

def loggedin(request) :

    return render_to_response('loggedin.html',
            {'full_name': request.user.username})

def logout(request) :
    
    auth.logout(request)
    return render_to_response('logout.html')

def register_user(request) :

    if (request.method == 'POST') :
        
        form = UserCreationForm(request.POST)

        if form.is_valid() :
            form.save()
            return HttpResponseRedirect('/accounts/register_success/')
    
    form = UserCreationForm()
    
    return render_to_response('register.html', {'form' : form},\
            context_instance=RequestContext(request))
            
def register_success(request) :

    return render_to_response('register_success.html')

def tictactoe(request) :

    if not request.user.is_authenticated() :

        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))

    if request.method == "POST" :
        
        if "sqr1" in request.POST :
            request.session["sqr1"] = "X"
        if "sqr2" in request.POST :
            request.session["sqr2"] = "X"
        if "sqr3" in request.POST :
            request.session["sqr3"] = "X"
        if "sqr4" in request.POST :
            request.session["sqr4"] = "X"
        if "sqr5" in request.POST :
            request.session["sqr5"] = "X"
        if "sqr6" in request.POST :
            request.session["sqr6"] = "X"
        if "sqr7" in request.POST :
            request.session["sqr7"] = "X"
        if "sqr8" in request.POST :
            request.session["sqr8"] = "X"
        if "sqr9" in request.POST :
            request.session["sqr9"] = "X"

    return render_to_response('tictactoe.html',\
            {'session' : request.session},\
            context_instance=RequestContext(request))
        

