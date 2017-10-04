from django.conf.urls import url
from .views import user_detail,home,user_fri,user_add_friends,user_accept_friend, user_decline_friend

urlpatterns = [
	url(r'^friends/decline/(?P<username>.+)/(?P<to_user>.+)/$',user_decline_friend,name='declinefriend'),
	url(r'^friends/accept/(?P<username>.+)/(?P<to_user>.+)/$',user_accept_friend,name='acceptfriend'),
	url(r'^friends/add/(?P<username>.+)/(?P<to_user>.+)/$',user_add_friends,name='addfriend'),
	url(r'^friends/(?P<username>.+)/$',user_fri,name='userfriends'),
	url(r'^(?P<username>.+)/$',user_detail,name='userdetail'),
	url(r'^$',home),
]