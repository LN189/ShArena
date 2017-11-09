from django.shortcuts import render,render_to_response,get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.http import HttpResponseRedirect,HttpResponse
from friendship.models import Friend
from friendship.models import FriendshipRequest
from chat.models import Room
from user_groups.models import project
from django.contrib.auth.models import User
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError, IntegrityError
from django.http import Http404
from .models import post,postingForm
from django.core.exceptions import MultipleObjectsReturned
from user_groups.models import profilePicture
from user_login.models import rating


@login_required
##@brief It just redirects the user to his home page view ::user_detail
def home(request):
    return HttpResponseRedirect(reverse('userdetail',args=[request.user.username]))

@login_required(login_url='/users/login/')
##@brief renders friends.html it lists the friends, sent friend requests, recieved friend requests with accept and delete button of requested user
#and also list of all users who are not friends to him so tha he can send friend requests.
#@param username name of the logged in user
def user_fri(request,username):
	user = get_object_or_404(User, username = username)
	friends = Friend.objects.friends(user)
	users = User.objects.all()
	unread = Friend.objects.unread_requests(user)
	sent = Friend.objects.sent_requests(user)
	sentfriends = [u.to_user for u in sent]
	return render(request,'user_login/friends.html', {'username': username,'sent' : sentfriends,'unread' : unread,'friends': friends,'users' : users, 'show_tags': True,'show_user': True})

@login_required(login_url='/users/login/')
##@brief It create a Friend object(make friends) betweeen the users and rediercts to the ::user_fri view
#@param username name of the friend request sent user
#@param username name of the friend request received user
def user_add_friends(request,username,to_user):
	from_user = get_object_or_404(User, username = username)
	to_user = get_object_or_404(User, username = to_user)
	try:
		req = Friend.objects.add_friend(from_user,to_user)
	except AlreadyExistsError:
		return redirect('userfriends',username = username)
	return redirect('userfriends',username = username)

@login_required(login_url='/users/login/')
##@brief it is called when user clicks accept on a friend request, it creates a friend object(make friends) and redirect to ::user_fri view
#@param username name of the friend request sent user
#@param username name of the friend request received user
def user_accept_friend(request, username, to_user):
	from_user = get_object_or_404(User, username = username)
	to_use = get_object_or_404(User, username = to_user)
	try :
		friend_request = FriendshipRequest.objects.get(from_user = to_use,to_user=from_user)
		friend_request.accept()
	except IntegrityError:
		friend_request.cancel()
		return redirect('userfriends',username = username)
	return redirect('userfriends',username = username)

@login_required(login_url='/users/login/')
##@brief it is called when user clicks delete  on a friend request, it deletes the friend object with that data and redirect to ::user_fri view
#@param username name of the friend request sent user
#@param username name of the friend request received user
def user_decline_friend(request, username, to_user):
    from_user = get_object_or_404(User, username = username)
    to_use = get_object_or_404(User, username = to_user)
    try:
        friend_request = FriendshipRequest.objects.get(from_user = to_use,to_user=from_user)
        friend_request.cancel()
        return redirect('userfriends',username = username)
    except IntegrityError:
        return redirect('userfriends',username = username)

@login_required(login_url='/users/login/')
##@brief It renders user.html , it is basically the home page of the user
# it conatins his rating, profile pic and links for friends and groups pages
#@param username username of the logged in user
def user_detail(request,username):
    user = get_object_or_404(User,username=username)
    status=0
    try:
        image=get_object_or_404(profilePicture,title=username)
        status=1
    except MultipleObjectsReturned:
        status=1
    except Http404:
        image=1
        status=0
    rates = rating.objects.filter(to_user = user)
    rateslist = list(map(lambda x:x.rate,rates))
    totalRating=0.0
    members=0
    for i in rateslist:
        totalRating=totalRating+float(i)
        members=members+1
    if(members==0):
        finalRate=0.0
    else:
        finalRate=totalRating/members
        finalRate = round(finalRate,1)
    return render(request,'user_login/user.html',{'status':status,'finalRate':finalRate})

@login_required(login_url='/users/login/')
##@brief It renders showrating.html it contains list of friends who are stil to be rated by him, u can rate them based on their work in the projects
#@param username name of the logged in user
def user_rating(request,username):
    user = get_object_or_404(User, username = username)
    friends = Friend.objects.friends(user)
    friendslist = list(map(lambda x:x.username,friends))
    print(friends)
    users = User.objects.all()
    unread = Friend.objects.unread_requests(user)
    sent = Friend.objects.sent_requests(user)
    rates = rating.objects.filter(from_user = user)
    rateslist = list(map(lambda x:x.to_user,rates))
    print(rateslist)
    stillRate=list(set(friends)-set(rateslist))
    print(stillRate)
    sentfriends = [u.to_user for u in sent]
    return render(request,'user_login/showrating.html', {'username': username,'sent' : sentfriends,'unread' : unread,'friends': friends,'users' : users,'stillRate':stillRate ,'show_tags': True,'show_user': True})

##@brief it recieves a post ajax request containing the rating model data,
#it creates a rating object between the to_user and from_user, it gets from_user from the url and to_user from the post request
#@param from_user username of the user who rated
def rateform(request,from_user):
    user1=get_object_or_404(User,username=from_user)
    if request.method == "POST":
        username2 = request.POST['to_user']
        rate = request.POST['ratevalue']
        to_user = get_object_or_404(User,username = username2)
        rateobj = rating(from_user = user1,to_user=to_user,rate=rate)
        rateobj.save()
        return HttpResponse("success")
    else :
        return HttpResponse("not a post")

##@brief it renders groupThread.html contains all the posts posted by the project members
#@Param projectname name of project whose groupThread should be displayed
#@param username name of the logged in user
def group_thread(request,username,projectname):
	posts = post.objects.filter(ofProject = projectname)
	return render(request,'user_login/groupThread.html', {'posts':posts,'user':username,'pro':projectname})

##@brief It receives a post request when someone posts a post in project groupThread, it validats the data if it is valid then adds post to group thread
#if it doesnt receive post reequest it renders postForm.html contains the form for posting post in group thread
#@param username name of the logged in user
#@param projectname title of the project
def add_post(request,username,projectname):
	if request.method == 'POST':
		form1 = postingForm(request.POST)
		if form1.is_valid():
			form = form1.save(commit = False)
			form.ofProject = projectname
			author=get_object_or_404(User,username=username)
			form.author = author
			form.save()
			return HttpResponseRedirect(reverse('groupThread',args=[username,projectname]))
	else:
		form = postingForm()
		return render(request,'user_login/postForm.html', {'form':form})

##@brief it renders profilePage which contains his name,rating,friends and projects he involved
#@param host username of the user whose profile u want to sentfriends
#@param guest name of the user who want to see who eants to see the host profile
def view_profile(request,guest,host):
    user = get_object_or_404(User,username=host)
    status=0
    try:
        image=get_object_or_404(profilePicture,title=host)
        status=1
    except MultipleObjectsReturned:
        status=1
    except Http404:
        image=1
        status=0
    rates = rating.objects.filter(to_user = user)
    rateslist = list(map(lambda x:x.rate,rates))
    totalRating=0.0
    rate1=0
    rate2=0
    rate3=0
    rate4=0
    rate5=0
    members=0
    for i in rateslist:
        totalRating=totalRating+float(i)
        if(float(i)==1):
            rate1=rate1+1
        if(float(i)==2):
            rate2=rate2+1
        if(float(i)==3):
            rate3=rate3+1
        if(float(i)==4):
            rate4=rate4+1
        if(float(i)==5):
            rate5=rate5+1
        members=members+1
    if(members==0):
        finalRate=0.0
    else:
        finalRate=totalRating/members
        finalRate = round(finalRate,1)
    pro = project.objects.filter(authors__in=[user]).values()
    friends = Friend.objects.friends(user)
    return render(request,'user_login/profilePage.html',{'pro':pro,'friends':friends,'status':status,'guest':guest,'host':host,'finalRate':finalRate,'members':members,'rate1':rate1,'rate2':rate2,'rate3':rate3,'rate4':rate4,'rate5':rate5})
