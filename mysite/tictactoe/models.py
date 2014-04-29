def check_you_win(session) :

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



       
