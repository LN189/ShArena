from django.shortcuts import render,render_to_response,get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.http import HttpResponseRedirect
from friendship.models import Friend
from friendship.models import FriendshipRequest
from chat.models import Room
from user_groups.models import project
from django.contrib.auth.models import User
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError, IntegrityError
from django.http import Http404
@login_required
def home(request):
    return HttpResponseRedirect(reverse('userdetail',args=[request.user.username]))

@login_required(login_url='/users/login/')
def user_fri(request,username):
	user = get_object_or_404(User, username = username)
	friends = Friend.objects.friends(user)
	users = User.objects.all()
	unread = Friend.objects.unread_requests(user)
	sent = Friend.objects.sent_requests(user)
	sentfriends = [u.to_user for u in sent]
	return render(request,'user_login/friends.html', {'username': username,'sent' : sentfriends,'unread' : unread,'friends': friends,'users' : users, 'show_tags': True,'show_user': True})

@login_required(login_url='/users/login/')
def user_add_friends(request,username,to_user):
	from_user = get_object_or_404(User, username = username)
	#friends = Friend.objects.friends(from_user)
	#users = User.objects.all()
	to_user = get_object_or_404(User, username = to_user)
	try:
		req = Friend.objects.add_friend(from_user,to_user)
	except AlreadyExistsError:
		return redirect('userfriends',username = username)
	return redirect('userfriends',username = username)
	#return render(request,'user_login/friends.html', {'username': username,'friends': friends,'users' : users, 'show_tags': True,'show_user': True})

@login_required(login_url='/users/login/')
def user_accept_friend(request, username, to_user):
	from_user = get_object_or_404(User, username = username)
	#friends = Friend.objects.friends(from_user)
	#users = User.objects.all()
	to_use = get_object_or_404(User, username = to_user)
	try :
		friend_request = FriendshipRequest.objects.get(from_user = to_use,to_user=from_user)
		room = Room(title='Chat',user1=from_user,user2=to_use)
		room.save()
		friend_request.accept()
	except IntegrityError:
		friend_request.cancel()
		return redirect('userfriends',username = username)
	return redirect('userfriends',username = username)

@login_required(login_url='/users/login/')
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
def user_detail(request,username):
	user = username
	return render(request,'user_login/user.html')

def room_creation(request,first_user,second_user):
	useri = get_object_or_404(User,username=first_user)
	userii = get_object_or_404(User,username=second_user)
	rooms1 = Room.objects.filter(user1 = useri)
	rooms2 = Room.objects.filter(user2 = useri)
	try:
		room = get_object_or_404(rooms1,user2=userii)
	except Http404:
		room = get_object_or_404(rooms2,user1=userii)
	return render(request,'user_login/showchat.html',{'first_user':first_user,'second_user':second_user,'room':room})
	
def group_chat_open(request,projectname):
	try:
		pro = get_object_or_404(project,title=projectname)
	except Http404:
		print('proerror')
	try:
		room = get_object_or_404(Room,title=projectname)
	except Http404:
		print('roomerror')
	return render(request,'user_login/groupchat.html',{'title':projectname,'room':room})

# Create your views here.
