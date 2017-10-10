from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
# Create your views here.
def home_page_view(request):
	template_name = 'user_login/homepage.html'
	return render(request,template_name)