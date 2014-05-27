
INSTALLATION INSTRUCTIONS
--------------------------

This is a Django app which requires standard Django setup with a few exceptions:


#1 :

TEMPLATE_CONTEXT_PROCESSORS = {
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request'
}


#2 :  

    I tested it out on MySQL, so can't guarantee it will work on SQL Lite


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'alex',
        'PASSWORD': 'cisco123',
        'HOST': '127.0.0.1',
        'PORT': '3306',        
    }
}

#3 :

    You need to add 'tictactoe' to the list of Django apps

#4 :

    Add the template dir to the list of template dirs:

TEMPLATE_DIRS = (
    '/home/alexander/Desktop/Django/templates',
)

#5: 

    This isn't relevant to Django per se, I wasn't able to find a way
    to source a local copy of JQuery from tictactoe.html, so I am still 
    loading it via HTTP. That may explain some initial delay in the game

#6:

    Make sure your browser security settings are medium or lower.
    It you set your security settings too high, not only popups
    won't work properly, but also Ajax requests will be blocked, so
    the buttons will not be updated correctly

HOW TO PLAY
-----------

The URL to start a new game is /tictactoe/new_game/
The URL to contiunue the previous game (or start a new one if it is
the first run) is /tictactoe/
You will be automatically redirected to the login page
You will need to register in the system in order to be able to play.
You will be redirected to the registration page from the login page
after you click 'register' button. After you register, you will need
to log in. Once you are logged in, just use mouse to click the buttons

The limitation of the current implementation is that the computer always 
hits the central square first, because it is the easiest and the fastest
way to win. The algorithm used is empirical, very popular, and is usually used 
when playing the game manually. I may be the first one to implement it in the code

Only single-user mode is currently supported
