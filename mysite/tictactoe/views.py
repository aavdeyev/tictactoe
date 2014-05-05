from django.shortcuts import render

# Create your views here.
from django import forms
from django.template import RequestContext

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from django.utils import timezone

from django.contrib.auth.models import User

from tictactoe.models import History

from tictactoelib import *

import json

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
# Function to display invalid user error
#
################################################################

def invalid(request) :

   return render_to_response('invalid.html',
           context_instance=RequestContext(request))

################################################################
#
# Function to authenticate a user
#
################################################################

def auth_view(request) :

    if "register" in request.POST :

        return HttpResponseRedirect('/accounts/register/')

    else :

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username = username, password = password)

        if user is not None :
            auth.login(request, user)
            return HttpResponseRedirect('/tictactoe/new_game')
        else :
            return HttpResponseRedirect('/accounts/invalid')

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

def start_new_game(request) :

    if not request.user.is_authenticated() :

        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))
    
    #---------------------------------------------------------------
    # Clear the key and reset status to 'continue'
    #---------------------------------------------------------------

    for key in ['sqr1','sqr2','sqr3','sqr4','sqr5','sqr6','sqr7',\
            'sqr8','sqr9'] :
        request.session[key] = ''

    request.session['status'] = 'CONTINUE'
    
    #---------------------------------------------------------------
    # Render the clean HTML page to the browser
    #---------------------------------------------------------------

    return render_to_response('tictactoe.html',\
            {'session' : request.session,\
                'status' : request.session['status'],\
                'player' : request.user.username},\
            context_instance=RequestContext(request))        
            
###################################################################
#
# The main view to handle user's mouse clicks during the game
# The view is using Ajax to update buttons asynchronously
#
###################################################################

def play_next_turn(request) :

    next_step = ''
    status = 'CONTINUE'
 
    if not request.user.is_authenticated() :

        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))

    if request.method == 'GET' :

        if request.GET.has_key('key_pressed') :
            key_pressed = request.GET['key_pressed']
            request.session[key_pressed] = 'X' 
        
            if check_user_won(request.session) : 
                #-----------------------------------------------------        
                # The user won
                #-----------------------------------------------------
                status = 'USERWON'
 
            else :
                #-----------------------------------------------------
                # Keep playing - take a turn
                #-----------------------------------------------------

                # Check to see if we can win in this turn
                next_step = try_attack(request.session) 
       
                if not next_step :
                    # If we can't win now, check to see if we need to 
                    # block the user from winning in this turn                    
                    next_step = try_defense(request.session)

                    if not next_step :
                        # If both procs above fail, just play randomly
                        next_step = try_random(request.session)
                                            
                # Update button info with the new computer-generated "O"                
                request.session[next_step] = 'O'  
 
                if check_user_lost(request.session) :                    
                    # The user lost                    
                    status = 'USERLOST'
                                        
        # Check if there is a draw        
        if check_draw(request.session) :            
            status = 'DRAW'

        #--------------------------------------------------------------
        # Save game result if game is complete
        #--------------------------------------------------------------
 
        if status != 'CONTINUE' :
            owner = User.objects.get(username=request.user.username).id 
            created = timezone.now()
  
            h = History(owner = owner, created = created, result = status)
            h.save() 
    
        #---------------------------------------------------------------
        # Build JSON to send back to the client
        #---------------------------------------------------------------

        json_reply = json.dumps({'next_step' : next_step,\
                'status' : status})
         
        return HttpResponse(json_reply, content_type='application/json')


def game_history(request) :

    history_html = ""
 
    if not request.user.is_authenticated() :

        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))

    if request.method == 'GET' :
        user_id = User.objects.get(username=request.user.username).id
        history_list = History.objects.filter(owner=user_id)

    return render_to_response('history.html',\
            {'player' : request.user.username,\
            'history_list' : history_list},\
            context_instance=RequestContext(request))
