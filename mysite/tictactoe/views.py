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

from game import *

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

##################################################################
#
# This will start a new game
#
##################################################################

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

    # Computer always starts by hitting the center
    request.session['sqr5'] = 'O'
    request.session['status'] = 'CONTINUE'
    # Computer has already completed step1 by hitting sqr5
    request.session['step_num'] = 2
    
    #---------------------------------------------------------------
    # Update the number of user's and computer's wins
    #---------------------------------------------------------------

    game_stats = get_game_history_stats(request)
    games_played = game_stats['games_played']
    user_wins = game_stats['user_wins']
    computer_wins = game_stats['computer_wins']
        
    #---------------------------------------------------------------
    # Render the clean HTML page to the browser
    #---------------------------------------------------------------

    return render_to_response('tictactoe.html',\
            {'session' : request.session,\
            'status' : request.session['status'],\
            'player' : request.user.username,\
            'games_played' : games_played,\
            'you_win' : user_wins,\
            'computer_wins' : computer_wins},\
            context_instance=RequestContext(request))        
            
###################################################################
#
# The main view to handle user's mouse clicks during the game.
# It is using Ajax/JSON to update buttons asynchronously
#
###################################################################

def play_next_turn(request) :
    
    if not request.user.is_authenticated() :
        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))
 
    if request.method == 'POST' :

        if request.POST.has_key('key_pressed'):
 
            # Read current step # from the session
            step_num = request.session['step_num']
           
            # Get user-pressed square id from JSON and save it 
            # in Django session
            usr_pressed = request.POST['key_pressed']
            request.session[usr_pressed] = 'X'
            
            if step_num == 2 :               
                result = step2(session = request.session,\
                        usr_step1 = usr_pressed)                
            elif step_num == 3 :
                result = step3(session = request.session,\
                        usr_step2 = usr_pressed)
            elif step_num == 4 :
                result = step4(session = request.session,\
                        usr_step3 = usr_pressed)
            elif step_num == 5 :
                result = step5(session = request.session,\
                        usr_step4 = usr_pressed)
                                    
            cmp_pressed = result['cmp_key']
            status = result['status']
            request.session['branch'] = result['branch']

            request.session[cmp_pressed] = 'O'
            request.session['step_num'] = step_num + 1
                                 
            print ("CMP " + cmp_pressed)

            #----------------------------------------------------------
            # Save game result if game is complete
            #----------------------------------------------------------
 
            if status != 'CONTINUE' :            
                owner = User.objects.get(username=request.user.username).id 
                created = timezone.now()
                  
                h = History(owner = owner, created = created, result = status)
                try:
                    h.save() 
                except Exception as err:
                    status = 'ERROR'                                 
            #-----------------------------------------------------------
            # Build JSON to send back to the client
            #-----------------------------------------------------------

            # Values to send to the client
            client_msg = {'next_step' : cmp_pressed, 'status' : status}

            if status in ('USER_LOST', 'USER_WON', 'DRAW') :
                
                # Add total number of wins/losses to the JSON
                game_stats = get_game_history_stats(request)
                client_msg['games_played'] = game_stats['games_played']
                client_msg['user_wins'] = game_stats['user_wins']
                client_msg['computer_wins'] = game_stats['computer_wins']
                           
            json_reply = json.dumps(client_msg)
         
            return HttpResponse(json_reply, content_type='application/json')

########################################################################
#
# The view to display game history
#
#########################################################################

def game_history(request) :

    history_html = ""
 
    if not request.user.is_authenticated() :
        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))
    
    # Read history records from database
    user_id = User.objects.get(username=request.user.username).id
    history_list = History.objects.filter(owner=user_id)

    # Pass history records back to the client
    return render_to_response('history.html',\
            {'player' : request.user.username,\
            'history_list' : history_list},\
            context_instance=RequestContext(request))

#########################################################################
#
# The view to clear game history
#
#########################################################################

def clear_history(request) :

    if not request.user.is_authenticated() :
        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))

    History.objects.all().delete()

    return game_history(request)

