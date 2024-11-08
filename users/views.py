from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from RateMovies.settings import EMAIL_HOST_USER
from django.views.generic import CreateView

from users.models import User
from users.forms import UserRegistrationForm
from .decorators import login_required, email_verif_required

import random
import string

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.verif_code = ''.join(random.choice(string.digits) for x in range(4))
            user.save()

            # send verification code to user's email
            code = user.verif_code
            subject = 'Verification Code Request'
            message = f'Here is your verification code {code}'
            recipient = [user.email]
            send_mail(subject, message, EMAIL_HOST_USER, recipient, fail_silently=False)
            messages.success(request, 'your account has been successfully created, please check your gmail for a code to activate your account')
            return HttpResponseRedirect(reverse('verify-user', kwargs={'username': user.username}))
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegistrationForm

    return render(request, 'users/register.html', {'form': form})


def verify_user(request, username):
    if request.method == "POST":
        code = request.POST.get('code')
        user = User.objects.get(username=username)
        if code == str(user.verif_code):
            user.is_verified = True
            user.save()
            messages.success(request, 'account verification successful')
            return redirect('movies-list')
        else:
            messages.info(request, 'account verification failed, invalid code')
            HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {}
    return render(request, 'users/verify_users.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        # check if user exists
        if user is not None:
            if user.is_verified == True:
                login(request, user)
                return redirect('movies-list')
            else: # send code to users again if they try logging into an inactive account
                code = user.verif_code
                subject = 'Verification Code Request'
                message = f'Here is your verification code {code}'
                recipient = [user.email]
                send_mail(subject, message, EMAIL_HOST_USER, recipient, fail_silently=False)
                messages.success(request, 'account is not yet verified, check your gmail for verification code')
                return HttpResponseRedirect(reverse('verify-user', kwargs={'username': user.username})) 
        else:
            messages.info(request, 'Invalid details, please ensure you entered the right email address and password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
    context = {}
    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')