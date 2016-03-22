from django.template import RequestContext
from django.shortcuts import render, redirect, render_to_response

def index(request):    
    if request.method == 'POST':
        print('lol')
    return render_to_response('launcher.html', {}, RequestContext(request))
