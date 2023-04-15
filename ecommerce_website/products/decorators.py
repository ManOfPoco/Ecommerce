from django.http import HttpResponseBadRequest


def is_ajax(function):
    def wrapper(request, *args, **kwargs):
        ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        print(request.POST)
        if ajax:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest('Invalid request')

    return wrapper
