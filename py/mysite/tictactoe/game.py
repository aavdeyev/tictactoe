from django.contrib.auth.models import User

from tictactoe.models import History, GameState

#######################################################################
#
#  Computer generated step 2 of the game
#
#  Input: 
#      user_step1 - Key pressed by the user in step 1 in 'sqrx' format
#  Returns:  
#      Dictionary of the following keys: 
#             computer_pressed : sqr<x>, 
#             branch : logical branch, 
#             status : 'USER_CONTINUE', 'USER_WON', 'USER_LOST' or 'DRAW'
# 
#######################################################################

def step2(user_step1) :

    if on_a_side(user_step1) :
        #---------------------------------------------------------------
        #  If combination is as follows, the user will lose
        #
        #               ? X ?
        #               ? O ?
        #               ? ? ?
        #
        #  We will name this logical branch usr_will_lose_1
        #---------------------------------------------------------------

        # We can put "O" in any corner, for example sqr1
        #
        #               O X ?
        #               ? O ?
        #               ? ? ?
        #

        return {'computer_pressed' : 'sqr1', 'branch' : 'usr_will_lose_1',\
                'status' : 'USER_CONTINUE',\
                'warning' : 'You just made a fatal mistake and will '\
                        'lose this game.'\
                        'You should never hit a side button in step 1'}

    else :
        #----------------------------------------------------------------
        #  The user still has a chance for a draw
        #
        #              ? ? X
        #              ? O ?
        #              ? ? ?
        #
        #  We will name this logical branch undetermined_1
        #------------------------------------------------------------------

        # Put "O" in the opposite corner from "X"
        #              ? ? X
        #              ? O ?
        #         O -> ? ? ?

        computer_step2 = opposite_corner(user_step1)
        return {'computer_pressed' : computer_step2,\
                'branch' : 'undetermined_1',\
                'status' : 'USER_CONTINUE'}

#######################################################################
#
#  Computer generated step 3 of the game
#
#  Input: 
#      sqrs - Dictionary of squares in format 'sqr<x>' : {'O'|'X'}
#      user_step2 - Key pressed by the user in step 2 in 'sqr<x>' format
#      branch - Logical branch
#  Returns:  
#      Dictionary with the following keys: 
#             computer_pressed : sqr<x>, 
#             branch : logical branch, 
#             status : 'USER_CONTINUE', 'USER_WON', 'USER_LOST' or 'DRAW'
# 
#######################################################################

def step3(sqrs, user_step2, branch) :

    if branch == 'usr_will_lose_1' :
        
        # Try winning in the third step if the user forgot to block
        # the "O O", for example :
        #        
        #             ? X O
        #             ? O X
        #        O -> ? ? ?          
        computer_step3 = win(sqrs)        
        if computer_step3 :
            return {'computer_pressed' : computer_step3,\
                    'branch' : 'usr_will_lose_1', 'status' : 'USER_LOST'}

        else : 
            # Complete winning triangle, for example, as follows:
            #
            #        ? X O
            #        ? O ?
            #        X ? ? <- O 
            computer_step3 = complete_winning_triangle(sqrs)
            status = 'USER_CONTINUE' 

            return {'computer_pressed' : computer_step3,\
                    'branch' : 'usr_will_lose_1', 'status' : 'USER_CONTINUE'}

    elif branch == 'undetermined_1' :
        
        if on_a_side(user_step2) :
             
            #-------------------------------------------------------------
            # The user will lose. We will name this branch usr_will_lose_2                        
            #-------------------------------------------------------------

            # Check to see if we have anything like this
            #
            #         O -> ? X X
            #              ? O ?
            #              O ? ?
            # If we do, we'll need to block the "XX"
            # Note that it will automatically build a winning triangle
          
            computer_step3 = block(sqrs)
                                                  
            if not computer_step3 :

                # Otherwise build a winning triangle, for example
                #         O -> ? ? X
                #              ? O ?
                #              O X ?                

                computer_step3 = complete_winning_triangle(sqrs)
            
            return {'computer_pressed' : computer_step3,\
                    'branch' : 'usr_will_lose_2',\
                    'status' : 'USER_CONTINUE',\
                    'warning' : 'You just made a fatal mistake and will'\
                            ' lose this game. You should never hit a'\
                            ' side button in step 2'}
        else :   
      
            #----------------------------------------------------
            # The user still has a chance for a draw
            #
            #              X ? X
            #              ? O ?
            #              O ? ?
            #----------------------------------------------------
 
            # We need to put O in between the two 'X's 
            computer_step3 = block(sqrs)

            return {'computer_pressed' : computer_step3,\
                    'branch' : 'undetermined_1',\
                    'status' : 'USER_CONTINUE'}

#######################################################################
#
#  Computer generated step 4 of the game
#
#  Input: 
#      sqrs - Dictionary of squares in format 'sqr<x>' : {'O'|'X'}
#      user_step3 - Key pressed by the user in step 3 in 'sqr<x>' format
#      branch - Logical branch
#  Returns:  
#      Dictionary with the following keys: 
#             computer_pressed : sqr<x>, 
#             branch : logical branch, 
#             status : 'USER_CONTINUE', 'USER_WON', 'USER_LOST' or 'DRAW'
# 
#######################################################################

def step4(sqrs, user_step3, branch) :

    if branch in ('usr_will_lose_1', 'usr_will_lose_2') :
        #--------------------------------------------------------------
        # We successfully built winning triangles in the previous step,
        # so just win now
        #--------------------------------------------------------------

        computer_step4 = win(sqrs)
    
        return {'computer_pressed' : computer_step4, 'branch' : branch,\
                'status' : 'USER_LOST'} 
                  
    elif branch == 'undetermined_1' :

        #----------------------------------------------------
        # Now our chance for victory is low, only if the user
        # makes an obvious error will we win
        #-----------------------------------------------------

        # Check to see if user made obvious error in previous step
        # by not blocking our 'O's
        #
        #  X O X
        #  ? O ?
        #  O ? ?
        #    ^
        #    | 
        #    O  
     
        computer_step4 = win(sqrs)

        # User lost
        if computer_step4 :
            return {'computer_pressed' : computer_step4,\
                    'branch' : 'undetermined_1',\
                    'status' : 'USER_LOST'}
        
        # If the user didn't lose yet, try hitting on a side
        #  X O X
        #  ? O ? <-- O
        #  O ? ?
        #
        # That will gives another chance to win if the user makes another
        # mistake

        if not sqrs.get('sqr2','') :
            computer_step4 = 'sqr2'
        elif not sqrs.get('sqr4','') :
            computer_step4 = 'sqr4'
        elif not sqrs.get('sqr6','') :
            computer_step4 = 'sqr6'
        elif not sqrs.get('sqr8','') :
            computer_step4 = 'sqr8'

        if not computer_step4 :        
            computer_step4 = hit_any(sqrs)

        return {'computer_pressed' : computer_step4,\
                    'branch' : 'undetermined_1',\
                    'status' : 'USER_CONTINUE'}

#######################################################################
#
#  Computer generated step 5 of the game
#
#  Input: 
#      sqrs - Dictionary of squares in format 'sqr<x>' : {'O'|'X'}
#      user_step4 - Key pressed by the user in step 4 in 'sqr<x>' format
#      branch - Logical branch
#  Returns:  
#      Dictionary with the following keys: 
#             computer_pressed : sqr<x>, 
#             branch : logical branch, 
#             status : 'USER_CONTINUE', 'USER_WON', 'USER_LOST' or 'DRAW'
# 
#######################################################################

def step5(sqrs, user_step4, branch) :

    # Check to see if we can still win
    #             X O X
    #      O -->  ? O O
    #             O X ?

    computer_step5 = win(sqrs)

    if computer_step5 :
        return {'computer_pressed' : computer_step5,\
               'branch' : 'undetermined_1',\
              'status' : 'USER_LOST'}

    # If we can't win, just hit any available square and get a draw       
    computer_step5 = hit_any(sqrs)
    
    return {'computer_pressed' : computer_step5,\
             'branch' : 'undetermined_1',\
             'status' : 'DRAW'}

########################################################################
#
#  Function to check if the square is located on a side, for example:
#
#      ? X ?    
#      ? ? ?
#      ? ? ?
#
#  Input:
#      sqr - square in format 'sqr<x>'
#  Returns:
#      True if on a side, False otherwise
#
########################################################################
                                                        
def on_a_side(sqr) :

    if sqr in ('sqr2','sqr4','sqr6','sqr8') :
        return True
    else :
        return False

def opposite_corner(sqr) :

    if sqr == 'sqr1' :
        return 'sqr9'
    elif sqr == 'sqr3' :
        return 'sqr7'
    elif sqr == 'sqr9' :
        return 'sqr1'
    elif sqr == 'sqr7' :
        return 'sqr3'

#################################################################
#
#  This function will try to build a winning triangle which
#  will give us victory in 2 steps. There are two possible types
#  of winning triangles (see below)
#
#      O X X                         
#      ? O ?      - Type 1 winnng triangle
#      O X X
#
#      O X X
#      ? O X      - Type 2 winning triangle
#      O X ?
#
#  Input: 
#       Dictionary of squares 'sqr<x>' : {'O'|'X'}
#
#  Returns:
#       Next step needed to complete the triangle in 'sqr<x>' format
#
##################################################################
    
def complete_winning_triangle(sqrs) :
   
    sqr1 = sqrs.get('sqr1','')
    sqr2 = sqrs.get('sqr2','')
    sqr3 = sqrs.get('sqr3','')
    sqr4 = sqrs.get('sqr4','')
    sqr5 = sqrs.get('sqr5','')
    sqr6 = sqrs.get('sqr6','')
    sqr7 = sqrs.get('sqr7','')
    sqr8 = sqrs.get('sqr8','')
    sqr9 = sqrs.get('sqr9','')

    # We assume that the center of the triangle is already ours
    # if not, just return ""
    if  not sqr5 :
        return ""

    #-----------------------------------------------------------
    # Check to see if we have potential type 1 winning triangles
    #----------------------------------------------------------

    if (sqr1 == "O") and not sqr2 and not sqr3 and not sqr8 :
        return 'sqr3'

    elif (sqr1 == "O") and not sqr4 and not sqr7 and not sqr6 :
        return 'sqr7'

    elif (sqr3 == "O") and not sqr1 and not sqr2 and not sqr8 :
        return 'sqr1'

    elif (sqr3 == "O") and not sqr6 and not sqr9 and not sqr4 :
        return 'sqr9'

    elif (sqr7 == "O") and not sqr4 and not sqr1 and not sqr6 :
        return 'sqr1'

    elif (sqr7 == "O") and not sqr8 and not sqr9 and not sqr2 :
        return 'sqr9'

    elif (sqr9 == "O") and not sqr8 and not sqr7 and not sqr2 :
        return 'sqr7'
    
    elif (sqr9 == "O") and not sqr3 and not sqr6 and not sqr4 :
        return 'sqr3'

    #-----------------------------------------------------------
    # Check to see if we have potential type 2 winning triangles
    #-----------------------------------------------------------

    if (sqr1 == "O") and not sqr2 and not sqr3 and not sqr7 :
        return 'sqr3'
 
    elif (sqr1 == "O") and not sqr4 and not sqr7 and not sqr3 :
        return 'sqr7'
  
    elif (sqr3 == "O") and not sqr1 and not sqr2 and not sqr9 :
        return 'sqr1'
 
    elif (sqr3 == "O") and not sqr6 and not sqr9 and not sqr1 :
        return 'sqr9'

    elif (sqr7 == "O") and not sqr4 and not sqr1 and not sqr9 :
        return 'sqr1'

    elif (sqr7 == "O") and not sqr8 and not sqr9 and not sqr1 :
        return 'sqr9'

    elif (sqr9 == "O") and not sqr8 and not sqr7 and not sqr3 :
        return 'sqr7'
    
    elif (sqr9 == "O") and not sqr3 and not sqr6 and not sqr7 :
        return 'sqr3'

    else :
        return ''

##################################################################
#
#  Win - See if we can win the game in this step
#
#  Input: 
#       Dictionary of squares 'sqr<x>' : {'O'|'X'}
#
#  Returns:
#       Next step needed to win the game
#
##################################################################

def win(sqrs) :

    sqr1 = sqrs.get('sqr1','')
    sqr2 = sqrs.get('sqr2','')
    sqr3 = sqrs.get('sqr3','')
    sqr4 = sqrs.get('sqr4','')
    sqr5 = sqrs.get('sqr5','')
    sqr6 = sqrs.get('sqr6','')
    sqr7 = sqrs.get('sqr7','')
    sqr8 = sqrs.get('sqr8','')
    sqr9 = sqrs.get('sqr9','')

    if sqr1 == 'O' and sqr2 == 'O' and not sqr3 :
        return 'sqr3'

    elif sqr2 == 'O' and sqr3 == 'O' and not sqr1 :
        return 'sqr1'

    elif sqr4 == 'O' and sqr5 == 'O' and not sqr6 :
        return 'sqr6'

    elif sqr5 == 'O' and sqr6 == 'O' and not sqr4 :
        return 'sqr4'

    elif sqr7 == 'O' and sqr8 == 'O' and not sqr9 :
        return 'sqr9'

    elif sqr8 == 'O' and sqr9 == 'O' and not sqr7 :
        return 'sqr7'

    elif sqr1 == 'O' and sqr5 == 'O' and not sqr9 :
        return 'sqr9'

    elif sqr5 == 'O' and sqr9 == 'O' and not sqr1 : 
        return 'sqr1'

    elif sqr3 == 'O' and sqr5 == 'O' and not sqr7 :
        return 'sqr7'

    elif sqr7 == 'O' and sqr5 == 'O' and not sqr3 :
        return 'sqr3'

    elif sqr1 == 'O' and sqr3 == 'O' and not sqr2 :
        return 'sqr2'

    elif sqr4 == 'O' and sqr6 == 'O' and not sqr5 :
        return 'sqr5'

    elif sqr7 == 'O' and sqr9 == 'O' and not sqr8 :
        return 'sqr8'

    elif sqr1 == 'O' and sqr7 == 'O' and not sqr4 :
        return 'sqr4'

    elif sqr2 == 'O' and sqr8 == 'O' and not sqr5 :
        return 'sqr5'

    elif sqr3 == 'O' and sqr9 == 'O' and not sqr6 :
        return 'sqr6'

    elif sqr1 == 'O' and sqr5 == 'O' and not sqr9 :
        return 'sqr9'

    elif sqr4 == 'O' and sqr7 == 'O' and not sqr1 :
        return 'sqr1'

    elif sqr5 == 'O' and sqr8 == 'O' and not sqr2 :
        return 'sqr2'

    elif sqr6 == 'O' and sqr9 == 'O' and not sqr3 :
        return 'sqr3'

    elif sqr1 == 'O' and sqr4 == 'O' and not sqr7 :
        return 'sqr7'

    elif sqr2 == 'O' and sqr5 == 'O' and not sqr8 :
        return 'sqr8'

    elif sqr3 == 'O' and sqr6 == 'O' and not sqr9 :
        return 'sqr9'

    elif sqr1 == 'O' and sqr9 == 'O' and not sqr5 :
        return 'sqr5'

    elif sqr3 == 'O' and sqr7 == 'O' and not sqr5 :
        return 'sqr5'

    else :
        return ''
  
##################################################################
#
#  Block - Block the user from completing a line and winning the game 
#      in the next step
#
#  Input: 
#       Dictionary of squares 'sqr<x>' : {'O'|'X'}
#
#  Returns:
#       Next step needed to block the user from winning
#
##################################################################

def block(sqrs) :
 
    sqr1 = sqrs.get('sqr1','')
    sqr2 = sqrs.get('sqr2','')
    sqr3 = sqrs.get('sqr3','')
    sqr4 = sqrs.get('sqr4','')
    sqr5 = sqrs.get('sqr5','')
    sqr6 = sqrs.get('sqr6','')
    sqr7 = sqrs.get('sqr7','')
    sqr8 = sqrs.get('sqr8','')
    sqr9 = sqrs.get('sqr9','')

    #-------------------------------------------------------------
    # Step1 : check to see if the user can win in the next turn,
    # and, if he can, block him
    #-------------------------------------------------------------

    if sqr1 == 'X' and sqr2 == 'X' and not sqr3 :
        return 'sqr3'

    elif sqr2 == 'X' and sqr3 == 'X' and not sqr1 :        
        return 'sqr1'

    elif sqr4 == 'X' and sqr5 == 'X' and not sqr6 :        
        return 'sqr6'

    elif sqr5 == 'X' and sqr6 == 'X' and not sqr4 :        
        return 'sqr4'

    elif sqr7 == 'X' and sqr8 == 'X' and not sqr9 :        
        return 'sqr9'

    elif sqr8 == 'X' and sqr9 == 'X' and not sqr7 :
        return 'sqr7'

    elif sqr1 == 'X' and sqr5 == 'X' and not sqr9 :
        return 'sqr9'

    elif sqr5 == 'X' and sqr9 == 'X' and not sqr1 : 
        return 'sqr1'

    elif sqr3 == 'X' and sqr5 == 'X' and not sqr7 :
        return 'sqr7'

    elif sqr7 == 'X' and sqr5 == 'X' and not sqr3 :
        return 'sqr3'

    elif sqr1 == 'X' and sqr3 == 'X' and not sqr2 :
        return 'sqr2'

    elif sqr4 == 'X' and sqr6 == 'X' and not sqr5 : 
        return 'sqr5'

    elif sqr7 == 'X' and sqr9 == 'X' and not sqr8 :
        return 'sqr8'

    elif sqr1 == 'X' and sqr7 == 'X' and not sqr4 : 
        return 'sqr4'

    elif sqr2 == 'X' and sqr8 == 'X' and not sqr5 :
        return 'sqr5'

    elif sqr3 == 'X' and sqr9 == 'X' and not sqr6 :
        return 'sqr6'

    elif sqr1 == 'X' and sqr5 == 'X' and not sqr9 :
        return 'sqr9'

    elif sqr4 == 'X' and sqr7 == 'X' and not sqr1 :
        return 'sqr1'

    elif sqr5 == 'X' and sqr8 == 'X' and not sqr2 :
        return 'sqr2'

    elif sqr6 == 'X' and sqr9 == 'X' and not sqr3 :
        return 'sqr3'

    elif sqr1 == 'X' and sqr4 == 'X' and not sqr7 : 
        return 'sqr7'

    elif sqr2 == 'X' and sqr5 == 'X' and not sqr8 :
        return 'sqr8'

    elif sqr3 == 'X' and sqr6 == 'X' and not sqr9 :
        return 'sqr9'

    elif sqr1 == 'X' and sqr9 == 'X' and not sqr5 :
        return 'sqr5'

    elif sqr3 == 'X' and sqr7 == 'X' and not sqr5 :
        return 'sqr5'

    #-------------------------------------------------------------
    # Step2 : Look 2 steps ahead and check to see if the user can 
    # win after 2 turns. If he can, do not let that happen     
    #-------------------------------------------------------------

    else :

        return ''

#################################################################
#
#  Just hit any button
#
#  Input: 
#       Dictionary of squares 'sqr<x>' : {'O'|'X'}
#
#  Returns:
#       hit_any square
#
##################################################################

def hit_any(sqrs) :
   
    sqr1 = sqrs.get('sqr1','')
    sqr2 = sqrs.get('sqr2','')
    sqr3 = sqrs.get('sqr3','')
    sqr4 = sqrs.get('sqr4','')
    sqr5 = sqrs.get('sqr5','')
    sqr6 = sqrs.get('sqr6','')
    sqr7 = sqrs.get('sqr7','')
    sqr8 = sqrs.get('sqr8','')
    sqr9 = sqrs.get('sqr9','')

    #--------------------------------------------------------------
    # Try center first to see if it already has a key assigned.
    # If it doesn't have, assign a key to it
    #--------------------------------------------------------------
    if not sqr5 :
        return 'sqr5'

    #---------------------------------------------------------------
    # Try corners if center isn't available
    #---------------------------------------------------------------
    elif not sqr1 :
        return 'sqr1'
  
    elif not sqr9 :
        return 'sqr9'

    elif not sqr3 :
        return 'sqr3'

    elif not sqr7 :
        return 'sqr7'

    #---------------------------------------------------------------
    # Try sides
    #---------------------------------------------------------------

    elif not sqr6 :        
        return 'sqr6'

    elif not sqr2 :
        return 'sqr2'

    elif not sqr8 :
        return 'sqr8'

    elif not sqr4 :
        return 'sqr4'

    else :
        return ''

########################################################################
#
# The fuction to return game history stats in a dictionary
#
#  Input:
#     Django request
#
#  Returns:
#      Dictionary of the following keys:
#          games_played : Number of games played so far
#          user_wins : Number of times user won so far
#          computer_wins : Number of times computer won so far
#          
########################################################################

def get_game_history_stats(request) :
   
    user_id = User.objects.get(username=request.user.username).id
    games_played = History.objects.filter(owner=user_id).count()
    user_wins = History.objects.filter(owner=user_id,\
            result='USER_WON').count()
    computer_wins = History.objects.filter(owner=user_id,\
            result='USER_LOST').count()

    return {'games_played' : games_played, 'user_wins' : user_wins,\
            'computer_wins' : computer_wins}

########################################################################
#
# The function to save current game state
#
#  Input:
#     Django request
#
#  Returns:
#      Dictionary of the following keys:
#          success : True on success, false on failure
#          error : Error message on error
#  
#########################################################################

def save_game_state(request) :
        
    user_id = User.objects.get(username=request.user.username).id
        
    session = request.session
    
    sqr1 = session.get("sqr1")   
    if not sqr1 :
        sqr1 = " "

    sqr2 = session.get("sqr2")   
    if not sqr2 :
        sqr2 = " "
    
    sqr3 = session.get("sqr3")   
    if not sqr3 :
        sqr3 = " "

    sqr4 = session.get("sqr4")   
    if not sqr4 :
        sqr4 = " "

    sqr5 = session.get("sqr5")   
    if not sqr5 :
        sqr5 = " "

    sqr6 = session.get("sqr6")   
    if not sqr6 :
        sqr6 = " "

    sqr7 = session.get("sqr7")   
    if not sqr7 :
        sqr7 = " "

    sqr8 = session.get("sqr8")   
    if not sqr8 :
        sqr8 = " "

    sqr9 = session.get("sqr9")  
    if not sqr9 :
        sqr9 = " "

    sqrs = sqr1 + sqr2 + sqr3 + sqr4 + sqr5 + sqr6 + sqr7\
            + sqr8 + sqr9

    # Delete previous game state
    GameState.objects.filter(owner=user_id).delete()

    created_print_str = session.get("created_print_str","")
           
    # Save the state for this game
    state_obj = GameState(owner = user_id, sqrs = sqrs,\
            branch = session['branch'],\
            step_num = session['step_num'],\
            status = session['status'],\
            created = created_print_str)

    try:
        state_obj.save()
        return {'success' : True, 'error' : ''}
    except Exception as err:
        return {'success' : False, 'error' : err}
    

