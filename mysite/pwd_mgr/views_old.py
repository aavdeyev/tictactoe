from django.shortcuts import render

from django.core.context_processors import csrf

# Create your views here.
from django import forms
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from pwd_mgr.models import Passwords
import datetime

from django.shortcuts import render_to_response

class passwordForm(forms.Form):

    userName = forms.CharField()
    userPasswd = forms.CharField()
    comments = forms.CharField()


def searchForm(request):

    return render_to_response('search_form.html')


def search(request):
    
    if 'q' in request.GET and request.GET['q']:

        q = request.GET['q']

        print ("Q: " + q)
        resultObjects = Passwords.objects.filter(userName=q)

        return render_to_response('search_results.html',\
                {'resultObjects' : resultObjects})
    else:
        print ("Error")

        return render_to_response('search_form.html',\
                {'error': True})


def searchFormPost(request):

    return render_to_response('search_form_post.html', context_instance=RequestContext(request) )

def search_post(request):

    errors = []

    if request.method == 'POST':

        print ("request.POST: " + request.POST['q'])

    c = {}
    c.update(csrf(request))

    return render_to_response('search_form_post.html', {'csrf_token' : c} )

    
def search_old(request):
    
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted and empty form.'

    return HttpResponse(message)


def testForm(request):

    form = passwordForm({'userName': 'Alex', 'userPasswd': 'Avdeev', 'comments': 'none'})

    return HttpResponse(form.as_ul())


def currentDateTime(request):
    
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    html = t.render(Context({'current_date' : now}))
    return HttpResponse(html)


def currentDateTime1(request):
    
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date' : now})


def getLocals(request):
    
    now = datetime.datetime.now()
    print ("*****************************************")
    print (locals())
    print ("*****************************************")
    return render_to_response('current_datetime.html', {'current_date' :locals()})
