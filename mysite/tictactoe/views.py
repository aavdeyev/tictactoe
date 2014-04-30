from django.shortcuts import render

# Create your views here.
from django import forms
from django.template import RequestContext

from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from tictactoelib import *

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

    print("Submitted")

    if not request.user.is_authenticated() :

        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))

    request.session["status"] = "continue"

    if request.method == "POST" :
        # Mark proper button with "X"       
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

        if check_user_won(request.session) == True :          

            # The user won            
            request.session["status"] = "USERWON"
 
        else :
            try_result_offense = try_offense(request.session)
         
            if try_result_offense["success"] == False :
                try_result_defense = try_defense(request.session)

                if try_result_defense["success"] == False :
                    try_result_random = try_random(request.session)
                    request.session = try_result_random["session"]
                    if check_user_lost(request.session) :
                        # The user lost
                        request.session["status"] = "USERLOST"
                    
                else :
                    request.session = try_result_defense["session"]                    
                    if check_user_lost(request.session) :
                        # The user lost
                        request.session["status"] = "USERLOST"
                        
            else :
                request.session = try_result_offense["session"]
                if check_user_lost(request.session) :
                    # The user lost
                    request.session["status"] = "USERLOST"

        if request.session["status"] in {"USERWON", "USERLOST"} :
            # Clear the buttons for a new game
            request.session["sqr1"] = ""
            request.session["sqr2"] = ""
            request.session["sqr3"] = ""
            request.session["sqr4"] = ""
            request.session["sqr5"] = ""
            request.session["sqr6"] = ""
            request.session["sqr7"] = ""
            request.session["sqr8"] = ""
            request.session["sqr9"] = ""
                    
    return render_to_response('tictactoe.html',\
            {'session' : request.session, 'status'\
                : request.session["status"]},\
            context_instance=RequestContext(request))
        

