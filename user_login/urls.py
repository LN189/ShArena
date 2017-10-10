from django.conf.urls import url
from .views import user_detail,home,user_fri,user_add_friends,user_accept_friend, user_decline_friend,room_creation, group_chat_open

urlpatterns = [
	url(r'^chat/(?P<first_user>.+)/(?P<second_user>.+)/$',room_creation,name='chatRoomCreation'),
	url(r'^groupChat/(?P<projectname>.+)/$',group_chat_open,name='groupChatOpen'),
	url(r'^friends/decline/(?P<username>.+)/(?P<to_user>.+)/$',user_decline_friend,name='declinefriend'),
	url(r'^friends/accept/(?P<username>.+)/(?P<to_user>.+)/$',user_accept_friend,name='acceptfriend'),
	url(r'^friends/add/(?P<username>.+)/(?P<to_user>.+)/$',user_add_friends,name='addfriend'),
	url(r'^friends/(?P<username>.+)/$',user_fri,name='userfriends'),
	url(r'^(?P<username>.+)/$',user_detail,name='userdetail'),
	url(r'^$',home),
]