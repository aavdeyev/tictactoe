def check_user_won(session) :

    sqr1 = session.get('sqr1',"").upper()
    sqr2 = session.get('sqr2',"").upper()
    sqr3 = session.get('sqr3',"").upper()
    sqr4 = session.get('sqr4',"").upper()
    sqr5 = session.get('sqr5',"").upper()
    sqr6 = session.get('sqr6',"").upper()
    sqr7 = session.get('sqr7',"").upper()
    sqr8 = session.get('sqr8',"").upper()
    sqr9 = session.get('sqr9',"").upper()

    if (sqr1 + sqr2 + sqr3 == "XXX") or (sqr4 + sqr5 + sqr6 == "XXX")\
            or (sqr7 + sqr8 + sqr9 == "XXX") or (sqr1 + sqr5 + sqr9 == "XXX")\
            or (sqr1 + sqr4 + sqr7 == "XXX") or (sqr2 + sqr5 + sqr8 == "XXX")\
            or (sqr3 + sqr6 + sqr9 == "XXX") or (sqr1 + sqr5 + sqr9 == "XXX")\
            or (sqr3 + sqr5 + sqr7 == "XXX") :

        return True
    else :              
        return False


def check_user_lost(session) :

    sqr1 = session.get('sqr1',"").upper()
    sqr2 = session.get('sqr2',"").upper()
    sqr3 = session.get('sqr3',"").upper()
    sqr4 = session.get('sqr4',"").upper()
    sqr5 = session.get('sqr5',"").upper()
    sqr6 = session.get('sqr6',"").upper()
    sqr7 = session.get('sqr7',"").upper()
    sqr8 = session.get('sqr8',"").upper()
    sqr9 = session.get('sqr9',"").upper()

    if (sqr1 + sqr2 + sqr3 == "OOO") or (sqr4 + sqr5 + sqr6 == "OOO")\
            or (sqr7 + sqr8 + sqr9 == "OOO") or (sqr1 + sqr5 + sqr9 == "OOO")\
            or (sqr1 + sqr4 + sqr7 == "OOO") or (sqr2 + sqr5 + sqr8 == "OOO")\
            or (sqr3 + sqr6 + sqr9 == "OOO") or (sqr1 + sqr5 + sqr9 == "OOO")\
            or (sqr3 + sqr5 + sqr7 == "OOO") :

        return True
    else :              
        return False

def check_draw(session) :

    sqr1 = session.get('sqr1',"").upper()
    sqr2 = session.get('sqr2',"").upper()
    sqr3 = session.get('sqr3',"").upper()
    sqr4 = session.get('sqr4',"").upper()
    sqr5 = session.get('sqr5',"").upper()
    sqr6 = session.get('sqr6',"").upper()
    sqr7 = session.get('sqr7',"").upper()
    sqr8 = session.get('sqr8',"").upper()
    sqr9 = session.get('sqr9',"").upper()

    if len(sqr1 + sqr2 + sqr3 + sqr4 + sqr5 + sqr6 + sqr7 + sqr8 + sqr9) == 9 :
        return True
    else :
        return False

def try_attack(session) :

    sqr1 = session.get('sqr1',"").upper()
    sqr2 = session.get('sqr2',"").upper()
    sqr3 = session.get('sqr3',"").upper()
    sqr4 = session.get('sqr4',"").upper()
    sqr5 = session.get('sqr5',"").upper()
    sqr6 = session.get('sqr6',"").upper()
    sqr7 = session.get('sqr7',"").upper()
    sqr8 = session.get('sqr8',"").upper()
    sqr9 = session.get('sqr9',"").upper()

    if sqr1 == "O" and sqr2 == "O" and not sqr3 :        
        session["sqr3"] = "O"
        return {'success': True, 'session' : session}

    elif sqr2 == "O" and sqr3 == "O" and not sqr1 :
        session["sqr1"] = "O"
        return {'success': True, 'session' : session}

    elif sqr4 == "O" and sqr5 == "O" and not sqr6 :
        session["sqr6"] = "O"
        return {'success': True, 'session' : session}

    elif sqr5 == "O" and sqr6 == "O" and not sqr4 :
        session["sqr4"] = "O"
        return {'success': True, 'session' : session}

    elif sqr7 == "O" and sqr8 == "O" and not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}

    elif sqr8 == "O" and sqr9 == "O" and not sqr7 :
        session["sqr7"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "O" and sqr5 == "O" and not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}

    elif sqr5 == "O" and sqr9 == "O" and not sqr1 :
        session["sqr1"] = "O" 
        return {'success': True, 'session' : session}         

    elif sqr3 == "O" and sqr5 == "O" and not sqr7 :
        session["sqr7"] = "O"
        return {'success': True, 'session' : session}        

    elif sqr7 == "O" and sqr5 == "O" and not sqr3 :
        session["sqr3"] = "O"
        return {'success': True, 'session' : session}        

    elif sqr1 == "O" and sqr3 == "O" and not sqr2 :
        session["sqr2"] = "O"
        return {'success': True, 'session' : session}        

    elif sqr4 == "O" and sqr6 == "O" and not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}        

    elif sqr7 == "O" and sqr9 == "O" and not sqr8 :
        session["sqr8"] = "O"
        return {'success': True, 'session' : session}      

    elif sqr1 == "O" and sqr7 == "O" and not sqr4 :
        session["sqr4"] = "O"
        return {'success': True, 'session' : session}

    elif sqr2 == "O" and sqr8 == "O" and not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}

    elif sqr3 == "O" and sqr9 == "O" and not sqr6 :
        session["sqr6"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "O" and sqr5 == "O" and not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}        

    elif sqr4 == "O" and sqr7 == "O" and not sqr1 :
        session["sqr1"] = "O"
        return {'success': True, 'session' : session}        

    elif sqr5 == "O" and sqr8 == "O" and not sqr2 :
        session["sqr2"] = "O"
        return {'success': True, 'session' : session}        

    elif sqr6 == "O" and sqr9 == "O" and not sqr3 :
        session["sqr3"] = "O"
        return {'success': True, 'session' : session}        

    elif sqr1 == "O" and sqr4 == "O" and not sqr7 :
        session["sqr7"] = "O"
        return {'success': True, 'session' : session}

    elif sqr2 == "O" and sqr5 == "O" and not sqr8 :
        session["sqr8"] = "O"
        return {'success': True, 'session' : session}

    elif sqr3 == "O" and sqr6 == "O" and not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "O" and sqr9 == "O" and not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}

    elif sqr3 == "O" and sqr7 == "O" and not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}

    else :
        return {'success': False, 'session' : session}

def try_defense(session) :

    sqr1 = session.get('sqr1',"").upper()
    sqr2 = session.get('sqr2',"").upper()
    sqr3 = session.get('sqr3',"").upper()
    sqr4 = session.get('sqr4',"").upper()
    sqr5 = session.get('sqr5',"").upper()
    sqr6 = session.get('sqr6',"").upper()
    sqr7 = session.get('sqr7',"").upper()
    sqr8 = session.get('sqr8',"").upper()
    sqr9 = session.get('sqr9',"").upper()

    if sqr1 == "X" and sqr2 == "X" and not sqr3 :
        session["sqr3"] = "O"
        return {'success': True, 'session' : session}

    elif sqr2 == "X" and sqr3 == "X" and not sqr1 :
        session["sqr1"] = "O"
        return {'success': True, 'session' : session}

    elif sqr4 == "X" and sqr5 == "X" and not sqr6 :
        session["sqr6"] = "O"
        return {'success': True, 'session' : session}

    elif sqr5 == "X" and sqr6 == "X" and not sqr4 :
        session["sqr4"] = "O"
        return {'success': True, 'session' : session}

    elif sqr7 == "X" and sqr8 == "X" and not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}

    elif sqr8 == "X" and sqr9 == "X" and not sqr7 :
        session["sqr7"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "X" and sqr5 == "X" and not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}

    elif sqr5 == "X" and sqr9 == "X" and not sqr1 :
        session["sqr1"] = "O"
        return {'success': True, 'session' : session}

    elif sqr3 == "X" and sqr5 == "X" and not sqr7 :
        session["sqr7"] = "O"
        return {'success': True, 'session' : session}

    elif sqr7 == "X" and sqr5 == "X" and not sqr3 :
        session["sqr3"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "X" and sqr3 == "X" and not sqr2 :
        session["sqr2"] = "O"
        return {'success': True, 'session' : session}

    elif sqr4 == "X" and sqr6 == "X" and not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}

    elif sqr7 == "X" and sqr9 == "X" and not sqr8 :
        session["sqr8"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "X" and sqr7 == "X" and not sqr4 :
        session["sqr4"] = "O"
        return {'success': True, 'session' : session}

    elif sqr2 == "X" and sqr8 == "X" and not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}

    elif sqr3 == "X" and sqr9 == "X" and not sqr6 :
        session["sqr6"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "X" and sqr5 == "X" and not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}

    elif sqr4 == "X" and sqr7 == "X" and not sqr1 :
        session["sqr1"] = "O"
        return {'success': True, 'session' : session}

    elif sqr5 == "X" and sqr8 == "X" and not sqr2 :
        session["sqr2"] = "O"
        return {'success': True, 'session' : session}

    elif sqr6 == "X" and sqr9 == "X" and not sqr3 :
        session["sqr3"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "X" and sqr4 == "X" and not sqr7 :
        session["sqr7"] = "O"
        return {'success': True, 'session' : session}

    elif sqr2 == "X" and sqr5 == "X" and not sqr8 :
        session["sqr8"] = "O"
        return {'success': True, 'session' : session}

    elif sqr3 == "X" and sqr6 == "X" and not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}

    elif sqr1 == "X" and sqr9 == "X" and not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}

    elif sqr3 == "X" and sqr7 == "X" and not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}

    else :
        return {'success': False, 'session' : session}

def try_random(session) :
    
    sqr1 = session.get('sqr1',"").upper()
    sqr2 = session.get('sqr2',"").upper()
    sqr3 = session.get('sqr3',"").upper()
    sqr4 = session.get('sqr4',"").upper()
    sqr5 = session.get('sqr5',"").upper()
    sqr6 = session.get('sqr6',"").upper()
    sqr7 = session.get('sqr7',"").upper()
    sqr8 = session.get('sqr8',"").upper()
    sqr9 = session.get('sqr9',"").upper()  

    if not sqr5 :
        session["sqr5"] = "O"
        return {'success': True, 'session' : session}

    elif not sqr1 :
        session["sqr1"] = "O"
        return {'success': True, 'session' : session}

    elif not sqr9 :
        session["sqr9"] = "O"
        return {'success': True, 'session' : session}

    elif not sqr3 :
        session["sqr3"] = "O"
        return {'success': True, 'session' : session}

    elif not sqr7 :
        session["sqr7"] = "O"
        return {'success': True, 'session' : session}

    elif not sqr6 :
        session["sqr6"] = "O"
        return {'success': True, 'session' : session}

    elif not sqr2 :
        session["sqr2"] = "O"
        return {'success': True, 'session' : session}

    elif not sqr8 :
        session["sqr8"] = "O"
        return {'success': True, 'session' : session}

    elif not sqr4 :
        session["sqr4"] = "O"
        return {'success': True, 'session' : session}

    else :
        return {'success': False, 'session' : session}
