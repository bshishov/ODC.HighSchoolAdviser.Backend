from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse
from .models import Subscriber

@csrf_protect
def index(request):    
    if request.method == 'POST':
        s = Subscriber(email=request.POST.get('email'), ip=get_client_ip(request))
        s.save()        
        return JsonResponse({ 'status' : "Спасибо" })
    return render_to_response('launcher.html', {}, RequestContext(request))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
