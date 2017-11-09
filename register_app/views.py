# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render,reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from friendship.models import Friend, Follow
from django.contrib.auth.models import User

##@brief it process the send post request while the user is logged in if it is valid it authenticates the user and redirects to the homepage of his
#if it dont receive a post request it simply renders signup.html
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('userdetail',args=[request.user.username]))
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
# Create your views here.
