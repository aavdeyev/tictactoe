from django.shortcuts import render

# Create your views here.
from django import forms
from django.template import RequestContext

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from tictactoelib import *

################################################################
#
# Function to Log user in
#
################################################################

def login(request) :

    return render_to_response('login.html',
            context_instance=RequestContext(request))

################################################################
#
# Function to authenticate a user
#
################################################################

def auth_view(request) :

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username = username, password = password)

    if user is not None :
        auth.login(request, user)
        return HttpResponseRedirect('/tictactoe/new_game')
    else :
        return HttpResponseRedirect('/accounts/invalid')

################################################################
#
# Function to display logged in screen
#
################################################################

def loggedin(request) :

    return render_to_response('loggedin.html',
            {'full_name': request.user.username})

#################################################################
#
# Function to display logout screen
#
#################################################################

def logout(request) :
    
    auth.logout(request)
    return render_to_response('logout.html')

##################################################################
#
# Function to register a new user
#
##################################################################

def register_user(request) :

    if (request.method == 'POST') :
        
        form = UserCreationForm(request.POST)

        if form.is_valid() :
            form.save()
            return HttpResponseRedirect('/accounts/register_success/')
    
    form = UserCreationForm()
    
    return render_to_response('register.html', {'form' : form},\
            context_instance=RequestContext(request))

###################################################################
#
# View to display registration success
#
###################################################################

def register_success(request) :

    return render_to_response('register_success.html')
            
###################################################################
#
# The main function to respond to user's mouse clicks during the game
#
###################################################################

def tictactoe(request) :
 
    if not request.user.is_authenticated() :

        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))

    # Always continue by default
    request.session["status"] = "CONTINUE"

    # Set this to True if the user pressed invalid button
    # and the turn needs to be skipped
    skip_turn = False

    if request.method == "POST" :
        #----------------------------------------------------------
        # Check for user's response and mark user-specified button 
        # with "X"
        #----------------------------------------------------------
        if "sqr1" in request.POST : 
            if not request.session.get("sqr1", "") :                           
                request.session["sqr1"] = "X"
            else :
                skip_turn = True
        if "sqr2" in request.POST :
            if not request.session.get("sqr2", "") :                
                request.session["sqr2"] = "X"
            else :
                skip_turn = True
        if "sqr3" in request.POST :
            if not request.session.get("sqr3", "") :               
                request.session["sqr3"] = "X"
            else :
                skip_turn = True
        if "sqr4" in request.POST :
            if not request.session.get("sqr4", "") :
                request.session["sqr4"] = "X"
            else :
                skip_turn = True
        if "sqr5" in request.POST :
            if not request.session.get("sqr5", "") :                
                request.session["sqr5"] = "X"
            else :
                skip_turn = True
        if "sqr6" in request.POST :            
            if not request.session.get("sqr6", "") :               
                request.session["sqr6"] = "X"
            else :
                skip_turn = True
        if "sqr7" in request.POST :           
            if not request.session.get("sqr7", "") :              
                request.session["sqr7"] = "X"
            else :
                skip_turn = True
        if "sqr8" in request.POST :            
            if not request.session.get("sqr8", "") :               
                request.session["sqr8"] = "X"
            else :
                skip_turn = True
        if "sqr9" in request.POST :           
            if not request.session.get("sqr9", "") :               
                request.session["sqr9"] = "X"
            else :
                skip_turn = True

        if not skip_turn :
        
            if check_user_won(request.session) == True :          
                #---------------------------------------------------
                # The user won
                #---------------------------------------------------
                request.session["status"] = "USERWON"
 
            else :
                #---------------------------------------------------
                # Keep playing - Make a turn
                #---------------------------------------------------

                # Check to see if it is a good time to attack
                # and win in this turn. If it is, play attack
                result = try_attack(request.session)         
                if result["success"] == False :

                    # If attack didn't work out, check to see if we
                    # need to prevent user from winning in this turn. 
                    # If we need, play defense
                    result = try_defense(request.session)
                    if result["success"] == False :

                        # Didn't find any opportunity for attack or
                        # defense, just play pseudo-randomly
                        result = try_random(request.session)
            
                #------------------------------------------------------
                # Update button info with the new computer-generated "O"
                #------------------------------------------------------
                request.session = result["session"]  

                #------------------------------------------------------
                # Check if user lost now
                #------------------------------------------------------
                if check_user_lost(request.session) :                
                    request.session["status"] = "USERLOST"
            
                #------------------------------------------------------
                # Check after computer's turn if there is a draw
                #------------------------------------------------------
                if check_draw(request.session) :            
                    request.session["status"] = "DRAW"
        
            #----------------------------------------------------------
            # Check after user's turn if there is a draw
            #----------------------------------------------------------
            if check_draw(request.session) :            
                request.session["status"] = "DRAW"

            #----------------------------------------------------------
            # Check to see if we need to clear buttons for a new game
            #----------------------------------------------------------
            if request.session["status"] != "CONTINUE" :
                request.session["sqr1"] = ""
                request.session["sqr2"] = ""
                request.session["sqr3"] = ""
                request.session["sqr4"] = ""
                request.session["sqr5"] = ""
                request.session["sqr6"] = ""
                request.session["sqr7"] = ""
                request.session["sqr8"] = ""
                request.session["sqr9"] = ""
    
    #------------------------------------------------------------------
    # Feed the HTML page to the browser
    #------------------------------------------------------------------
    return render_to_response('tictactoe.html',\
            {'session' : request.session, 'status'\
                : request.session["status"]},\
            context_instance=RequestContext(request))
        

