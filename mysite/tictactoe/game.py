from django.contrib.auth.models import User

from tictactoe.models import History

#######################################################################
#
#  Computer generated step2
#
#     Input: Key user pressed in step 1 in 'sqrx' format
#     Output:  Dictionary with the followin keys: cmp_key, branch and 
#             status
# 
#######################################################################

def step2(usr_step1) :

    if on_a_side(usr_step1) :
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

        return {'cmp_key' : 'sqr1', 'branch' : 'usr_will_lose_1',\
                'status' : 'CONTINUE'}

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

        cmp_step2 = opposite_corner(usr_step1)
        return {'cmp_key' : cmp_step2, 'branch' : 'undetermined_1',\
                'status' : 'CONTINUE'}


def step3(sqrs, usr_step2, branch) :

    if branch == 'usr_will_lose_1' :
        
        # Try winning in the third step if the user forgot to block
        # the "O O", for example :
        #        
        #             ? X O
        #             ? O X
        #        O -> ? ? ?          
        cmp_step3 = win(sqrs)        
        if cmp_step3 :
            return {'cmp_key' : cmp_step3, 'branch' : 'usr_will_lose_1', 'status' : 'USER_LOST'}

        else : 
            # Complete winning triangle, for example, as follows:
            #
            #        ? X O
            #        ? O ?
            #        X ? ? <- O 
            cmp_step3 = complete_winning_triangle(sqrs)
            status = 'CONTINUE' 

            return {'cmp_key' : cmp_step3, 'branch' : 'usr_will_lose_1', 'status' : 'CONTINUE'}

    elif branch == 'undetermined_1' :
        
        if on_a_side(usr_step2) :
             
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
          
            cmp_step3 = block(sqrs)
                                                  
            if not cmp_step3 :

                # Otherwise build a winning triangle, for example
                #         O -> ? ? X
                #              ? O ?
                #              O X ?                

                cmp_step3 = complete_winning_triangle(sqrs)
            
            return {'cmp_key' : cmp_step3, 'branch' : 'usr_will_lose_2',\
                    'status' : 'CONTINUE'}
        else :   
      
            #----------------------------------------------------
            # The user still has a chance for a draw
            #
            #              X ? X
            #              ? O ?
            #              O ? ?
            #----------------------------------------------------
 
            # We need to put O in between the two 'X's 
            cmp_step3 = block(sqrs)

            return {'cmp_key' : cmp_step3, 'branch' : 'undetermined_1',\
                    'status' : 'CONTINUE'}


def step4(sqrs, usr_step3, branch) :

    if branch in ('usr_will_lose_1', 'usr_will_lose_2') :
        # Proceed to the next step to win
        cmp_step4 = win(sqrs)
    
        return {'cmp_key' : cmp_step4, 'branch' : branch,\
                'status' : 'USER_LOST'} 
                  
    elif branch == 'undetermined_1' :

        #----------------------------------------------------
        # Now our chance for victory is low, only if the user
        # makes an obvious error will we win
        #-----------------------------------------------------

        cmp_step4 = win(sqrs)

        # User lost
        if cmp_step4 :
            return {'cmp_key' : cmp_step4, 'branch' : 'undetermined_1',\
                    'status' : 'USER_LOST'}
        
        # Try to hit on a side
        if not sqrs.get('sqr2','') :
            cmp_step4 = 'sqr2'
        elif not sqrs.get('sqr4','') :
            cmp_step4 = 'sqr4'
        elif not sqrs.get('sqr6','') :
            cmp_step4 = 'sqr6'
        elif not sqrs.get('sqr8','') :
            cmp_step4 = 'sqr8'

        if not cmp_step4 :        
            cmp_step4 = random(sqrs)

        return {'cmp_key' : cmp_step4, 'branch' : 'undetermined_1',\
                    'status' : 'CONTINUE'}

def step5(sqrs, usr_step4, branch) :

    cmp_step5 = win(sqrs)

    if cmp_step5 :
        return {'cmp_key' : cmp_step5, 'branch' : 'undetermined_1',\
              'status' : 'USER_LOST'}

    cmp_step5 = random(sqrs)
    
    return {'cmp_key' : cmp_step5, 'branch' : 'undetermined_1',\
             'status' : 'DRAW'}
                                                        
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

    if sqr1 and not sqr2 and not sqr3 and not sqr8 :
        return 'sqr3'

    elif sqr1 and not sqr4 and not sqr7 and not sqr6 :
        return 'sqr7'

    elif sqr3 and not sqr1 and not sqr2 and not sqr8 :
        return 'sqr1'

    elif sqr3 and not sqr6 and not sqr9 and not sqr4 :
        return 'sqr9'

    elif sqr7 and not sqr4 and not sqr1 and not sqr6 :
        return 'sqr1'

    elif sqr7 and not sqr8 and not sqr9 and not sqr2 :
        return 'sqr9'

    elif sqr9 and not sqr8 and not sqr7 and not sqr2 :
        return 'sqr7'
    
    elif sqr9 and not sqr3 and not sqr6 and not sqr4 :
        return 'sqr3'

    else :
        return ''
 
####################################################################
#
# The proc to check if the user has won
#
# Input - Django sqrs
# Returns - True or False
#
####################################################################

def check_user_won(sqrs) :

    sqr1 = sqrs.get('sqr1','')
    sqr2 = sqrs.get('sqr2','')
    sqr3 = sqrs.get('sqr3','')
    sqr4 = sqrs.get('sqr4','')
    sqr5 = sqrs.get('sqr5','')
    sqr6 = sqrs.get('sqr6','')
    sqr7 = sqrs.get('sqr7','')
    sqr8 = sqrs.get('sqr8','')
    sqr9 = sqrs.get('sqr9','')

    if (sqr1 + sqr2 + sqr3 == 'XXX') or (sqr4 + sqr5 + sqr6 == 'XXX')\
            or (sqr7 + sqr8 + sqr9 == 'XXX') or (sqr1 + sqr5 + sqr9 == 'XXX')\
            or (sqr1 + sqr4 + sqr7 == 'XXX') or (sqr2 + sqr5 + sqr8 == 'XXX')\
            or (sqr3 + sqr6 + sqr9 == 'XXX') or (sqr1 + sqr5 + sqr9 == 'XXX')\
            or (sqr3 + sqr5 + sqr7 == 'XXX') :

        return True
    else :              
        return False

#####################################################################
#
# The proc to check if the user has lost
#
#  Input - Django sqrs
#  Returns - True or False
#
#####################################################################

def check_user_lost(sqrs) :

    sqr1 = sqrs.get('sqr1','')
    sqr2 = sqrs.get('sqr2','')
    sqr3 = sqrs.get('sqr3','')
    sqr4 = sqrs.get('sqr4','')
    sqr5 = sqrs.get('sqr5','')
    sqr6 = sqrs.get('sqr6','')
    sqr7 = sqrs.get('sqr7','')
    sqr8 = sqrs.get('sqr8','')
    sqr9 = sqrs.get('sqr9','')

    if (sqr1 + sqr2 + sqr3 == 'OOO') or (sqr4 + sqr5 + sqr6 == 'OOO')\
            or (sqr7 + sqr8 + sqr9 == 'OOO') or (sqr1 + sqr5 + sqr9 == 'OOO')\
            or (sqr1 + sqr4 + sqr7 == 'OOO') or (sqr2 + sqr5 + sqr8 == 'OOO')\
            or (sqr3 + sqr6 + sqr9 == 'OOO') or (sqr1 + sqr5 + sqr9 == 'OOO')\
            or (sqr3 + sqr5 + sqr7 == 'OOO') :

        return True
    else :              
        return False

#################################################################
#
# The proc to check if there is a draw
#
#  Input - Django sqrs
#  Returns - True or False
#
#################################################################

def check_draw(sqrs) :

    sqr1 = sqrs.get('sqr1','')
    sqr2 = sqrs.get('sqr2','')
    sqr3 = sqrs.get('sqr3','')
    sqr4 = sqrs.get('sqr4','')
    sqr5 = sqrs.get('sqr5','')
    sqr6 = sqrs.get('sqr6','')
    sqr7 = sqrs.get('sqr7','')
    sqr8 = sqrs.get('sqr8','')
    sqr9 = sqrs.get('sqr9','')

    if len(sqr1 + sqr2 + sqr3 + sqr4 + sqr5 + sqr6 + sqr7 + sqr8 + sqr9) == 9 :
        return True
    else :
        return False

##################################################################
#
#  Win - win in this step if possible
#
#  Input - Django sqrs
#  Returns - Suggested next step (sqrX)
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
#  Block - Block the user from completing the line
#
#  Input - Django sqrs
#  Returns - Suggesed next step (sqrX) 
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
#  Just take random step 
#
#  Input - Django sqrs
#  Returns - Next step (sqrX)
#
##################################################################

def random(sqrs) :
   
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
# The proc to return game history stats in a dictionary
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
    
