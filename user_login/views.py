from django.shortcuts import render,render_to_response,get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.http import HttpResponseRedirect
from friendship.models import Friend
from friendship.models import FriendshipRequest
from django.contrib.auth.models import User
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError, IntegrityError

@login_required
def home(request):
    return HttpResponseRedirect(reverse('userdetail',args=[request.user.username]))

def user_fri(request,username):
	user = get_object_or_404(User, username = username)
	friends = Friend.objects.friends(user)
	users = User.objects.all()
	unread = Friend.objects.unread_requests(user)
	sent = Friend.objects.sent_requests(user)
	return render(request,'user_login/friends.html', {'username': username,'sent' : sent,'unread' : unread,'friends': friends,'users' : users, 'show_tags': True,'show_user': True})

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

def user_accept_friend(request, username, to_user):
	from_user = get_object_or_404(User, username = username)
	#friends = Friend.objects.friends(from_user)
	#users = User.objects.all()
	to_use = get_object_or_404(User, username = to_user)
	try :
		friend_request = FriendshipRequest.objects.get(from_user = to_use,to_user=from_user)
		friend_request.accept()
	except IntegrityError:
		friend_request.cancel()
		return redirect('userfriends',username = username)
	return redirect('userfriends',username = username)

def user_detail(request,username):
	user = username
	return render(request,'user_login/user.html')
# Create your views here.
