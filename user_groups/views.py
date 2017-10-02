from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView,DetailView
from .models import project, projectform,textfile,textfileForm
import os,sys
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def group(request):
	return HttpResponseRedirect(reverse('usergroups',args=[request.user.username]))
# Create your views here.

#def groups_view(request,username):
	#user = username
	#return render(request,'user_login/groups.html')

class groups_view(ListView):
	model = project
	def get(self,request,username):
		template_name = 'user_login/groups.html'
		user = get_object_or_404(User,username=username)		
		pro = project.objects.filter(authors__in=[user]).values()
		l = [x for x in pro]
		print(l)
		print(4)
		return render(request,template_name,{'projects' : pro})

def new_project(request,username):
	user = username
	if request.method == 'POST':
		form = projectform(request.POST)
		if form.is_valid():
			form.save();
			return HttpResponseRedirect(reverse('usergroups',args=[user]))
	else :
		form = projectform()
	return render(request,'user_login/newproject.html',{'form' : form})

def upload_file(request,username,project):
	user=get_object_or_404(User,username=username)
	pro=project
	if request.method == 'POST':
		form1 = textfileForm(request.POST, request.FILES)
		if form1.is_valid():
			form = form1.save(commit = False)
			form.user = user
			form.pro = pro
			form.save()
			return HttpResponseRedirect(reverse('fileslist',args=[user.username,pro]))
	else:
		form = textfileForm()
	return render(request, 'user_login/uploadfile.html', {'form': form})

def files_view(request,username,projectname):
	user = username
	curruser = get_object_or_404(User,username=username)
	pro = projectname
	pro1 = project.objects.filter(authors__in=[curruser])
	print(pro1)
	currpro = get_object_or_404(pro1,title=pro)
	members=currpro.authors.all()
	#try:
	#	members=project.objects.get(title=pro)
	#except project.MultipleObjectsReturned:
	#	i=0;
	#	while(i>=0):
	#		members=project.objects.get(title=pro).order_by('id')[0]
	#		if members.objects.authors__in==[user]:
	#			break
	path = 'media/user_' + str(user) + '/' + str(pro) + '/'
	try:
		files = os.listdir(path)
	except FileNotFoundError:
		files=[]
	return render(request,'user_login/projectdetails.html',{'files' : files,'user' : user , 'pro' :pro, 'members' : members})		

