#
#
# Create your views here
#
#

from django.shortcuts import render

from django import forms
from django.template import RequestContext

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from tictactoe.models import History, GameState

from game import *

import datetime

import json

##################################################################
#
# Function to Log user in
#
##################################################################

def login(request) :

    if request.method == 'POST' :

        if "register" in request.POST :

            #----------------------------------------------------------
            # The user clicked Register button
            #----------------------------------------------------------

            return HttpResponseRedirect('/accounts/register/')

        else :

            #----------------------------------------------------------
            # The user clicked Login button
            #----------------------------------------------------------
        
            form = AuthenticationForm(None, request.POST)
           
            if form.is_valid() :                
                # Log the user in
                auth.login(request, form.get_user())
                                
                # The 'next' query string parameter will be set to the 
                # current absolute path by @login_required. Redirect 
                # to the current absolute path or, if not specified, 
                # to /tictactoe/new_game/
                query_string = request.META.get('QUERY_STRING')
                if query_string :
                    redirect_url = query_string.replace('next=', '')
                else :
                    redirect_url = '/tictactoe/load_game/'
                
                return HttpResponseRedirect(redirect_url)   
    else:

        #------------------------------------------------------------
        # Initial form or error display
        #------------------------------------------------------------

        form = AuthenticationForm()
  
    return render_to_response('login.html', {'form' : form},\
            context_instance=RequestContext(request))

#################################################################
#
# Function to display logout screen
#
#################################################################

def logout(request) :
    
    error = ''

    # Save game state in a database. If fails, set error to display
    # in the logout page
    result = save_game_state(request)
    if not result['success'] :         
        error = result['error']

    auth.logout(request)
    return render_to_response('logout.html', {'error' : error})

##################################################################
#
# Function to register a new user
#
##################################################################

def register_user(request) :
  
    if request.method == 'POST' :

        if "login" in request.POST :          
            #-----------------------------------------------------
            # The user clicked Login button
            #-----------------------------------------------------

            return HttpResponseRedirect('/accounts/login/')

        else:            
            #-----------------------------------------------------
            # The user clicked Register button
            #-----------------------------------------------------
        
            form = UserCreationForm(request.POST)

            if form.is_valid() :
                form.save()
                return HttpResponseRedirect('/accounts/register_success/')                    
    else :
        #-----------------------------------------------------------
        # Initial form or error display
        #----------------------------------------------------------

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
# This view will load the last saved game or reload the current game
#
###################################################################

@login_required
def load_game(request) :
     
    if not request.session.get('status','') :

        #----------------------------------------------------------
        # Game stats don't exist, so we will either load the last
        # saved game or, if there is none, create a new one
        #----------------------------------------------------------

        user_id = User.objects.get(username=request.user.username).id
        games_saved = GameState.objects.filter(owner=user_id).count()

        if games_saved :
            #
            # We have a game saved
            #

            last_game = GameState.objects.get(owner=user_id)
        
            request.session['step_num'] = last_game.step_num
            request.session['status'] = last_game.status
            request.session['branch'] = last_game.branch
            request.session['created_print_str'] =\
                    str(last_game.created)

            sqrs = last_game.sqrs
            for i in range(0, 9) :                       
                request.session['sqr' + str(i+1)] = sqrs[i].strip()

            #
            # Update the number of user's and computer's wins
            #

            game_stats = get_game_history_stats(request)
            games_played = game_stats['games_played']
            user_wins = game_stats['user_wins']
            computer_wins = game_stats['computer_wins']

            status = request.session['status']
                                            
            # Render the page to the browser                          
            return render_to_response('tictactoe.html',\
                    {'status' : status,\
                    'player' : request.user.username,\
                    'games_played' : games_played,\
                    'you_win' : user_wins,\
                    'computer_wins' : computer_wins},\
                    context_instance=RequestContext(request))
        else :

            #
            # No saved games found, start a new game
            #

            return start_new_game(request)
    else :

        #-------------------------------------------------------
        # Game status found. That means there is a game in progress.
        # Reload the current game
        #-------------------------------------------------------
        
        status = request.session['status']
  
        game_stats = get_game_history_stats(request)
        games_played = game_stats['games_played']
        user_wins = game_stats['user_wins']
        computer_wins = game_stats['computer_wins']

        # Render the page to the browser
        return render_to_response('tictactoe.html',\
                {'status' : status,\
                'player' : request.user.username,\
                'games_played' : games_played,\
                'you_win' : user_wins,\
                'computer_wins' : computer_wins},\
                context_instance=RequestContext(request))
          
##################################################################
#
# This view will start a new game
#
##################################################################

@login_required
def start_new_game(request) :
  
    #----------------------------------------------------------
    # Clear the keys and reset status to 'continue'
    #----------------------------------------------------------
 
    # Button values will be stored under session as 'sqrx' keys
    for key in ['sqr1','sqr2','sqr3','sqr4','sqr5','sqr6','sqr7',\
            'sqr8','sqr9'] :
        request.session[key] = ''

    # Computer always starts by hitting the center (square #5)
    request.session['sqr5'] = "O"  
    # Computer has already completed step1 by hitting square #5
    request.session['step_num'] = 2

    request.session['status'] = 'USER_CONTINUE'
    request.session['branch'] = ''

    # Save game start time
    now = datetime.datetime.now()
    request.session['created'] = str(now)

    # This will be the formatted display start time
    print_time = now.strftime("%Y-%m-%d %H:%M:%S")
    request.session['created_print_str'] = print_time 

    # Load the new game
    return HttpResponseRedirect('/tictactoe/load_game/')
                
###################################################################
#
# The main view to handle user's mouse clicks during the game.
# It is using Ajax/JSON to update buttons asynchronously
#
###################################################################

@login_required
def play_next_turn(request) :
      
    if request.method == 'POST' :

        if request.POST.has_key('user_pressed'):

            if request.session['status'] != 'USER_CONTINUE' :
                json_reply =\
                        json.dumps({'status' : request.session['status'],\
                        'game_over' : 'true'})                          
                # Tell the client that the game is over
                return HttpResponse(json_reply,\
                        content_type='application/json')
           
            # Read current step # from the session
            step_num = request.session['step_num']
           
            # Get user-pressed square id from JSON and save it 
            # in Django session
            usr_pressed = request.POST['user_pressed']
            
            request.session[usr_pressed] = 'X'

            # Build keylist to pass over to the step procs
            sqrs = {}
            for key in ['sqr1', 'sqr2', 'sqr3', 'sqr4', 'sqr5', 'sqr6',\
                    'sqr7', 'sqr8', 'sqr9'] :
                sqrs[key] = request.session.get(key,'')
 
            # Execute proper function to play the step            
            if step_num == 2 :               
                result = step2(user_step1 = usr_pressed)               
            elif step_num == 3 :
                result = step3(sqrs = sqrs, user_step2 = usr_pressed,\
                        branch = request.session['branch'])
            elif step_num == 4 :
                result = step4(sqrs = sqrs, user_step3 = usr_pressed,\
                        branch = request.session['branch'])
            elif step_num == 5 :
                result = step5(sqrs = sqrs, user_step4 = usr_pressed,\
                        branch = request.session['branch'])
                                        
            computer_pressed = result['computer_pressed']         
            warning = result.get('warning','')

            request.session['branch'] = result['branch']
            request.session[computer_pressed] = 'O'
            request.session['step_num'] = step_num + 1
            request.session['status'] = result['status']
       
            #----------------------------------------------------------
            # Save game result if game is complete
            #----------------------------------------------------------
 
            if request.session['status'] != 'USER_CONTINUE' :            
                owner =\
                    User.objects.get(username=request.user.username).id
                created = timezone.now()
                  
                h = History(owner = owner, created = created,\
                        result = request.session['status'])
                try:
                    h.save() 
                except Exception as err:
                    request.session['status'] = 'ERROR' 
 
            #-----------------------------------------------------------
            # Build JSON to send back to the client
            #-----------------------------------------------------------

            # Values to send to the client
            client_msg = {'computer_pressed' : computer_pressed,\
                    'status' : request.session['status']}
            
            if request.session['status'] in ('USER_LOST', 'USER_WON', 'DRAW') :
                # Add total number of wins/losses to the JSON
                game_stats = get_game_history_stats(request)
                client_msg['games_played'] = game_stats['games_played']
                client_msg['user_wins'] = game_stats['user_wins']
                client_msg['computer_wins'] = game_stats['computer_wins']

            if warning :
                client_msg['warning'] = warning
                           
            json_reply = json.dumps(client_msg)
                                      
            # Send JSON back to the browser
            return HttpResponse(json_reply, content_type='application/json')

########################################################################
#
# The view to display game history
#
#########################################################################

@login_required
def game_history(request) :

    history_html = ""
    hist_error = ""
  
    # Read history records from database
    try:
        user_id = User.objects.get(username=request.user.username).id
        history_list = History.objects.filter(owner=user_id)                    
    except Exception as err:
        hist_error = "Error retrieving game history: " + str(err)
  
    # Pass history records back to the client
    return render_to_response('history.html',\
            {'player' : request.user.username,\
             'hist_error' : hist_error,\
            'history_list' : history_list},\
            context_instance=RequestContext(request))

#########################################################################
#
# The view to clear game history
#
#########################################################################

@login_required
def clear_history(request) :

    History.objects.all().delete()

    # Display clean history page
    return game_history(request)

##########################################################################
#
# The view to continue game when "Back to Game" button is pressed
#
##########################################################################

@login_required
def back_to_game(request) :
             
    #---------------------------------------------------------------
    # Update the number of user's and computer's wins
    #---------------------------------------------------------------

    game_stats = get_game_history_stats(request)
    games_played = game_stats['games_played']
    user_wins = game_stats['user_wins']
    computer_wins = game_stats['computer_wins']

    status = request.session['status']
       
    #---------------------------------------------------------------
    # Render the page to the browser
    #---------------------------------------------------------------

    return render_to_response('tictactoe.html',\
            {'status' : request.session['status'],\
            'player' : request.user.username,\
            'games_played' : games_played,\
            'you_win' : user_wins,\
            'computer_wins' : computer_wins},\
            context_instance=RequestContext(request))

    
