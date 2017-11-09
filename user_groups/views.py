from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from .models import project, projectform,textfile,textfileForm,merge_requests
import os,sys
from django.conf import settings
from chat.models import Room
from .models import project
from friendship.models import Friend
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import profilePicture, profilePicForm
import os
import json
from user_login.models import projectrequest


@login_required(login_url='/users/login/')
## @brief just to redirect the logged in user to his groups page view groups_view
def group(request):
	return HttpResponseRedirect(reverse('usergroups',args=[request.user.username]))

## @brief View of his groups page renders groups.html which contains
# list of projects he involded in,
# sent project requests , requets send for his project
class groups_view(ListView):
	model = project
	def get(self,request,username):
		template_name = 'user_login/groups.html'
		user = get_object_or_404(User,username=username)
		pro = project.objects.filter(authors__in=[user]).values()
		l = [x for x in pro]
		return render(request,template_name,{'projects' : pro})

## @brief view of his projects and projects request he can approve and projects to which he can send request
# maintains 4 lists in this process that consists of his projects,projects he can accept,projects he can send request to,his project requests
# the above 4 lists can be got by operating on objects of projectrequest,project and filtering them based on user presence
def getgroups(request,username):
	user = get_object_or_404(User,username=username)
	template_name = 'user_login/groups.html'
	projectreqs = projectrequest.objects.all()
	project_rtitles=list(map(lambda x:x.to_pro,projectreqs))
	project_from = list(map(lambda x:x.from_user,projectreqs))
	prtitles =[]
	for x in project_rtitles:
		l=[]
		l.append(x)
		prtitles.append(l);
	it = 0;
	for x in prtitles:
		prtitles[it].append(project_from[it])
		it = it+1
	print(prtitles)
	print(project_rtitles)
	send_objects = projectrequest.objects.filter(from_user=user)
	send_rtitles = list(map(lambda x:x.to_pro,send_objects))
	projects=list(map(lambda x:get_object_or_404(project,title=x),project_rtitles))
	proc = project.objects.filter(authors__in=[user])
	pro = project.objects.filter(authors__in=[user]).values()
	pror1 = list(map(lambda x:x.title,proc))
	print(pro)
	troll =[]
	count = 0;
	for x in project_rtitles:
		try:
			b=pror1.index(x)
		except ValueError:
			troll=troll
		else:
			troll.append(prtitles[count])
		count = count+1
	prolist = list(map(lambda x:x['title'],pro))
	pro1 = project.objects.all()
	pro1list = list(map(lambda x:x.title,pro1))
	process = list(set(pro1list)-set(prolist))
	process = list(set(process)-set(send_rtitles))
	process1 =[]
	for x in process:
		l=[]
		l.append(x)
		process1.append(l);
	var = 0;
	for x in process:
		ject = get_object_or_404(project,title=x)
		if ject.description!="":
			process1[var].append("Description: "+ject.description)
		else:
			process1[var].append("Description: None")
		var = var+1;
	print(process1)
	return render(request,template_name,{'projects' : pro,'send':send_rtitles,'accept':troll,'allprojects' : process1})

##@brief it adds the requested user to the project
#@param user1 logged in user
#@param username username of the user form which the request has been sent to the project
#@param projectname title of the project
def accepting(request,user1,username,projectname):
	user = get_object_or_404(User,username=username)
	pro = project.objects.filter(title=projectname).first()
	pro.authors.add(user)
	instance = get_object_or_404(projectrequest,to_pro=projectname,from_user=user).delete()
	return HttpResponseRedirect(reverse('usergroups',args=[user1]))

##@brief ir deletes the projectrequest object if present with the data and redirect to groups_view
#@param user1 logged in user
#@param username username of the user form which the request has been sent
#@param projectname title of the project
def deleting(request,user1,username,projectname):
	user = get_object_or_404(User,username=username)
	instance = projectrequest.objects.get(to_pro=projectname,from_user=user)
	instance.delete()
	return HttpResponseRedirect(reverse('usergroups',args=[user1]))

##@brief it creates a projectrequest object with the data in the request
#@param user1 logged in user
#@param username username of the user form which the request has been sent
#@param projectname title of the project
def send_project(request,user,projectname):
	user1 = get_object_or_404(User,username=user)
	req = projectrequest(from_user=user1,to_pro=projectname)
	req.save();
	return HttpResponseRedirect(reverse('usergroups',args=[user1]))


@login_required(login_url='/users/login/')
## @brief View for the project form projectform for creating a project
#it recieves a post request then it does form valdation of the post data
#if it is valid then it creates the project model with that data and redirect to his groups page groups_view
#and if it is empty it renders newproject.html if it is post request and if the  valid data then
def new_project(request,username):
	user = username
	if request.method == 'POST':
		form = projectform(request.POST)
		if form.is_valid():
			form.save();
			data = str(form.cleaned_data['title'])
			useri = get_object_or_404(User,username=user)
			room = Room(title=data,user1=useri,user2=useri)
			room.save()
			return HttpResponseRedirect(reverse('usergroups',args=[user]))
	else :
		form = projectform()
	return render(request,'user_login/newproject.html',{'form' : form})


@login_required(login_url='/users/login/')
## @brief view for the file form textfileForm for uploading a new file
#it recieves a post request then it does form valdation of the post data
#if it is valid then it stores the file based on the function models.py::user_directory_path and redirect to his project page ::file_view
#if it is empty it renders uploadfile.html
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

@login_required(login_url='/users/login/')
## @brief view for the project page renders projectdeatils.html it lists all the files in project, members associated to project
# and friends not in project so that you can add them in to your project if you wanr
def files_view(request,username,projectname):
	user = username
	curruser = get_object_or_404(User,username=username)
	pro = projectname
	friends = Friend.objects.friends(curruser)
	print(friends)
	pro1 = project.objects.filter(authors__in=[curruser])
	print(pro1)
	currpro = get_object_or_404(pro1,title=pro)
	members=currpro.authors.all()
	path = 'media/user_' + str(user) + '/' + str(pro) + '/'
	try:
		files = os.listdir(path)
		print(files)
	except FileNotFoundError:
		files=['No files uploaded yet']
		print(files)
	return render(request,'user_login/projectdetails.html',{'friends' : friends,'files' : files,'user' : user , 'pro' :pro, 'members' : members})

@login_required(login_url='/users/login/')
## @brief view renders files_details.html for listing the files of the user you want
#@param mainUser username of the whose files you want to see
#@param username username of the looged in user
def list_files(request,mainUser,username,projectname):
	user = username
	pro = projectname
	try :
		path = 'media/user_' + str(user) + '/' + str(pro) + '/'
		files = os.listdir(path)
		print(files)
	except FileNotFoundError:
		files = ['No files uploaded yet']
	return render(request,'user_login/files_details.html',{'files' : files ,'mainUser':mainUser, 'user' : user , 'pro' : pro})

## @brief It simply for adding a member into a project and redirect to ::fileslist view
#@param username Username of logged in user
#@param to_username username of the user u wanted to add into the project
#@parsam projectname title of the project to to_user would be added
def add_member(request,username,projectname,to_username):
	pro = projectname
	curruser = get_object_or_404(User,username = username)
	projects = project.objects.filter(authors__in = [curruser])
	currpro = get_object_or_404(projects,title = pro)
	to_user =  get_object_or_404(User,username = to_username)
	currpro.authors.add(to_user)
	return HttpResponseRedirect(reverse('fileslist',args=[curruser.username,pro]))

## @brief view renders openfile.html it basically opens the file in the project from database
# and also lists all the mergerequests came to that file and a mergerequest form for merging your code with other project member file
#@param filename name of the file to be opened
#@param projectname title of the project of file
def file_view(request,username,projectname,filename) :
	path = 'media/user_' + str(username) + '/' + str(projectname) + '/' + str(filename)
	codedmatter = open(path,"r")
	matter = codedmatter.read()
	user =username
	user = get_object_or_404(User,username=user)
	pro = get_object_or_404(project,title=projectname)
	mergerequests = merge_requests.objects.filter(to_user=user)
	members = pro.authors.all()
	files = ""
	return render(request,'user_login/openfile.html',{'ms':mergerequests,'files':files,'members':members,'matter' : matter ,'path':path,'projectname':projectname,'filename' :filename,'username' :username})

@csrf_protect
##@brief it recieves a post ajax request whenever a key is pressed in ::file_view it saves the data from the post request in the reqquested file
#@param filename name of the file in which data should be saved
def file_saving(request,username,projectname,filename) :
#return HttpResponse("no")
	if request.method=="POST" :
		matter = request.POST['updatedmatter']
		#path = 'media/user_' + str(usernam) + '/' + str(projectnam) + '/' + str(filenam)
		path = request.POST['path']
		file = open(path,'w')
		file.write(matter)
		file.close
		return HttpResponse(matter)
	else :
		return HttpResponse("noz")

##@brief it renders othersview,html it openns the file of reqquested user
#@param username username of the user whose file you want to open
#@param filename name of the file u want to open in users project files
def others_view(request,username,projectname,filename) :
	if request.method == "POST" :
		path = request.POST['pat']
		codedmatter = open(path,"r")
		matter = codedmatter.read()
		return HttpResponse(matter)
	else :
		path = 'media/user_' + str(username) + '/' + str(projectname) + '/' + str(filename)
		codedmatter = open(path,"r")
		matter = codedmatter.read()
		#matter = "<br>".join(matter.split("\n"))
		return render(request,'user_login/othersview.html',{'path' : path,'matter' : matter,'user' : username,'pro' : projectname,'filename' : filename})

##@brief It deletes the requested fiel of the user
def delete_file(request,username,projectname,filename) :
	path = 'media/user_' + str(username) + '/' + str(projectname) + '/' + str(filename)
	os.remove(path)
	return HttpResponseRedirect(reverse('fileslist',args=[username,projectname]))

##@brief it deletes the project object if present with that data
#@Param username username of the logged user
#@param projectname title of the project
def delete_project(request,username,projectname) :
	pro = get_object_or_404(project,title=projectname).delete()
	return HttpResponseRedirect(reverse('groups'))

##@brief renders foem @link profilePicForm @endlink for uploading the profile pic of the user
def upload_pic(request,username):
	user=get_object_or_404(User,username=username)
	if request.method == 'POST':
		form1 = profilePicForm(request.POST, request.FILES)
		if form1.is_valid():
			form = form1.save(commit = False)
			form.user = user
			form.title = username
			form.save()
			status=1
			image=get_object_or_404(profilePicture,title=username)
			return render(request,'user_login/user.html',{'status': status})
	else:
		form = profilePicForm()
	return render(request, 'user_login/uploadfile.html', {'form': form})

#@app.route('/user_groups')
## @brief It recieves a post ajax request form file_view on clicking a user so that it returns the list of files of that in the project
#param username username of the user whose files u want to list
def merge_files(request,username,projectname,filename):
	user = request.POST['usernam']
	pro = projectname
	path = 'media/user_' + str(user) + '/' + str(pro) + '/'
	files = os.listdir(path)
	#print(json.dumps(files))
	return HttpResponse(json.dumps(files))

##@brief It recieves a post ajax request form the file_view when deleting or accepting a merge request
#for deleting it simply delete the mergerequests object associated with two users(will be in the post request)
#after accepting it takes the data in merge request and places the data in file with the help of ::merge()
def merge_type(request,username,projectname,filename):
	if request.method == "POST" :
		#print("1")
		data = request.POST['matter']
		user = username
		requser = request.POST['user']
		from_user = get_object_or_404(User,username=requser)
		to_user = get_object_or_404(User,username=username)
		title = request.POST['title1']
		print(requser)
		pro =projectname
		mergetype = request.POST['type']
		if (mergetype == "delete"):
			mergeobj = merge_requests.objects.get(from_user=from_user,to_user=to_user,data=data,title=title,filename=filename)
			mergeobj.delete()
			return HttpResponse("deleted")
		if (mergetype == "accept") :
			file1 = filename
			path = 'media/user_' + str(user) + '/' + str(pro) + '/' + str(file1)
			val=merge(path,requser,data,title)
			with open(path,'w') as file:
				file.write(val);
			return HttpResponse(val)
	else :
		return HttpResponse(" not a post ")

##@brief it takes data and searches for sentence "@merge usernmae title" replaces that line with the data
#@param s path of the file to which data should be added
#@param title title of the merge request
#@param name username of the send user of merge request
def merge(s,name,data,title):
	val = ""
	with open(s,'r') as file:
		content = file.readlines();
		for x in content:
			if x.lstrip(' ').find("@merge")!=-1:
				st1=x.lstrip(' ').lstrip("@merge").lstrip(" ").rstrip("\n");
				st1=st1.rstrip(' ');
				if(st1.find(name)!=-1):
					st1=st1.lstrip(name).lstrip(" ");
					if(st1==title):
						val+="\n"+data+"\n\n";
					else:
						val+=x;
				else:
					val+=x;
			else:
				if x.find("@merge")==-1:
					val+=x;
	return val;

@login_required(login_url='/users/login/')
##@brief It recieves a post ajax request from the openfile.html page contains a merge request data it checks if alla fields are there , if not it wont create mergerequests object with data else it will create a mergerequests object
def file_merge(request,username,projectname,filename):
	#user = get_object_or_404(User,username = username)
	if request.method == "POST":
		title2 = request.POST['title1']
		username1 = request.POST.get("to_user1")
		print(username1)
		if title2 == "" :
		 	return HttpResponse("No Title")

		if (username1 == "") :
			return HttpResponse("No To_user")
		print(title2)

		to_user2 = get_object_or_404(User,username =username1)
		username2 = request.POST.get('from_user1')
		from_user2 = get_object_or_404(User,username=username2)
		filename2 = request.POST['filename1']
		if (filename2 == "") :
			return HttpResponse("No filename")
		data2 = request.POST['data1']
		mergeobj = merge_requests(title=title2,from_user=from_user2,to_user=to_user2,data=data2,filename=filename2)
		mergeobj.save()
		return HttpResponse("success")
	else:
		return HttpResponse("something wrong")
