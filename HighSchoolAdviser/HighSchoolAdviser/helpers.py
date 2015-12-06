from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.loader import render_to_string

def render(request, path, context = {}):
    return render_to_response(path, context, RequestContext(request))

def render_json(context):
    import json
    return HttpResponse(json.dumps(context), content_type = 'application/json')

def get_int_param(request, param_name):
    param_name = request.query_params.get(param_name)
    return int(param_name) if param_name else 0

def get_int_param(request, param_name):
    param_name = request.GET.get(param_name, 0)
    return int(param_name) if param_name else 0

def get_user_units(request):
    unit = {}
    user = request.user
    if user.is_authenticated():
        unit['russian'] = user.user_info.russian
        unit['math'] = user.user_info.math
        unit['physics'] = user.user_info.physics
        unit['chemistry'] = user.user_info.chemistry
        unit['informatics'] = user.user_info.informatics
        unit['biology'] = user.user_info.biology
        unit['history'] = user.user_info.history
        unit['geography'] = user.user_info.geography
        unit['foreign_language'] = user.user_info.foreign_language
        unit['social_science'] = user.user_info.social_science
        unit['literature'] = user.user_info.literature
        unit['specs'] = user.user_info.specs
    else:
        unit['russian'] = request.session.get('russian', 0)
        unit['math'] = request.session.get('math', 0)
        unit['physics'] = request.session.get('physics', 0)
        unit['chemistry'] = request.session.get('chemistry', 0)
        unit['informatics'] = request.session.get('informatics', 0)
        unit['biology'] = request.session.get('biology', 0)
        unit['history'] = request.session.get('history', 0)
        unit['geography'] = request.session.get('geography', 0)
        unit['foreign_language'] = request.session.get('foreign_language', 0)
        unit['social_science'] = request.session.get('social_science', 0)
        unit['literature'] = request.session.get('literature', 0)
        unit['specs'] = request.session.get('specs', None)
    return unit

def set_user_units(request):
    unit = {}
    user = request.user
    unit['russian'] = get_int_param(request, 'russian')
    unit['math'] = get_int_param(request, 'math')
    unit['physics'] = get_int_param(request, 'physics')
    unit['chemistry'] = get_int_param(request, 'chemistry')
    unit['informatics'] = get_int_param(request, 'informatics')
    unit['biology'] = get_int_param(request, 'biology')
    unit['history'] = get_int_param(request, 'history')
    unit['geography'] = get_int_param(request, 'geography')
    unit['foreign_language'] = get_int_param(request, 'foreign_language')
    unit['social_science'] = get_int_param(request, 'social_science')
    unit['literature'] = get_int_param(request, 'literature')
    unit['specs'] = [int(s) for s in request.GET.getlist('specs')]
    request.session['russian'] = unit['russian']
    request.session['math'] = unit['math']
    request.session['physics'] = unit['physics']
    request.session['chemistry'] = unit['chemistry']
    request.session['informatics'] = unit['informatics']
    request.session['biology'] = unit['biology']
    request.session['history'] = unit['history']
    request.session['geography'] = unit['geography']
    request.session['foreign_language'] = unit['foreign_language']
    request.session['social_science'] = unit['social_science']
    request.session['literature'] = unit['literature']
    request.session['specs'] = unit['specs']
    if user.is_authenticated():
        user.user_info.russian = unit['russian']
        user.user_info.math = unit['math']
        user.user_info.physics = unit['physics']
        user.user_info.chemistry = unit['chemistry']
        user.user_info.informatics = unit['informatics']
        user.user_info.biology = unit['biology']
        user.user_info.history = unit['history']
        user.user_info.geography = unit['geography']
        user.user_info.foreign_language = unit['foreign_language']
        user.user_info.social_science = unit['social_science']
        user.user_info.literature = unit['literature']
        user.user_info.specs = unit['specs']
        user.user_info.save()
    return unit

def put_user_info_into_session(request):
    user = request.user
    if user.is_authenticated():
        request.session['russian'] = user.user_info.russian
        request.session['math'] = user.user_info.math
        request.session['physics'] = user.user_info.physics
        request.session['chemistry'] = user.user_info.chemistry
        request.session['informatics'] = user.user_info.informatics
        request.session['biology'] = user.user_info.biology
        request.session['history'] = user.user_info.history
        request.session['geography'] = user.user_info.geography
        request.session['foreign_language'] = user.user_info.foreign_language
        request.session['social_science'] = user.user_info.social_science
        request.session['literature'] = user.user_info.literature
        request.session['specs'] = user.user_info.specs

def count_user_points(units, plan):
    return units['russian'] * plan.russian + \
        units['math'] * plan.math + \
        units['physics'] * plan.physics + \
        units['chemistry'] * plan.chemistry + \
        units['informatics'] * plan.informatics + \
        units['biology'] * plan.biology + \
        units['history'] * plan.history + \
        units['geography'] * plan.geography + \
        units['foreign_language'] * plan.foreign_language + \
        units['social_science'] * plan.social_science + \
        units['literature'] * plan.literature

def require_post(function=None, url='/'):
    def _decorator(view_function):
        def _view(request, *args, **kwargs):
            if request.method == 'POST':
                #do some before the view is reached stuffs here.
                return view_function(request, *args, **kwargs)
            else:
                return redirect(url)

        _view.__name__ = view_function.__name__
        _view.__dict__ = view_function.__dict__
        _view.__doc__ = view_function.__doc__

        return _view

    if function:
        return _decorator(function)
    return _decorator

def require_login(function=None, url='/'):
    def _decorator(view_function):
        def _view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_function(request, *args, **kwargs)
            else:
                return redirect(url)

        _view.__name__ = view_function.__name__
        _view.__dict__ = view_function.__dict__
        _view.__doc__ = view_function.__doc__

        return _view

    if function:
        return _decorator(function)
    return _decorator

def unauthenticated_only(function=None, url='/'):
    def _decorator(view_function):
        def _view(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return view_function(request, *args, **kwargs)
            else:
                return redirect(url)

        _view.__name__ = view_function.__name__
        _view.__dict__ = view_function.__dict__
        _view.__doc__ = view_function.__doc__

        return _view

    if function:
        return _decorator(function)
    return _decorator