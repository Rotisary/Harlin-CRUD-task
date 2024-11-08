from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings


def login_required(*args, **kwargs):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('login'))
        return wrapper_func
    return decorator


def email_verif_required(*args, **kwargs):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_verified:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('login'))
        return wrapper_func
    return decorator