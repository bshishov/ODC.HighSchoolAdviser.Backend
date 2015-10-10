import json

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.loader import render_to_string

def render(request, path, context = {}):
    return render_to_response(path, context, RequestContext(request))

def render_json(context):
    return HttpResponse(json.dumps(context), content_type = 'application/json')