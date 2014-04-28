from django.shortcuts import render

# from django.core.context_processors import csrf

# Create your views here.
from django import forms
from django.template import RequestContext

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from pwd_mgr.models import pwdMgrModel
from pwd_mgr.forms import pwdMgrModelForm

from django.utils import timezone
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

#################### App User Management functions #################

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
        
##################### PWD MGR specific functions #####################
        
def add_user(request) :

    if not request.user.is_authenticated() :

        # Unathenticated user, redirect the user to the login page
        return render_to_response('login.html',
                context_instance=RequestContext(request))
    
    if request.method == 'POST' :

        form = pwdMgrModelForm(request.POST)
        
        if form.is_valid() :        
            model_instance = form.save(commit=False)

            # Add id number for the current logged in web user
            model_instance.owner =\
                User.objects.get(username=request.user.username).id

            # Add record creation time
            model_instance.created = timezone.now()
            model_instance.save()
            
            return render_to_response('continue.html')
        else :            
            return render_to_response('add_user.html',\
                    {'form' : form.as_p(),\
                    'username' : request.user.username},
                    context_instance=RequestContext(request))

    else:

        form = pwdMgrModelForm()

        return render_to_response('add_user.html',\
                {'form' : form.as_p(),\
                'username' : request.user.username},\
                context_instance=RequestContext(request))


