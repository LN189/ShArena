from django.conf.urls import url, include
from .views import user_detail,home,user_fri,user_add_friends,user_rating,user_accept_friend, user_decline_friend, rateform, group_thread, add_post, view_profile

urlpatterns = [
	url(r'^userrating/(?P<from_user>.+)/rate/$',rateform,name='ratingform'),
	url(r'^userrating/(?P<username>.+)/$',user_rating,name='userrating'),
	url(r'^ViewProfile/(?P<guest>.+)/(?P<host>.+)/$',view_profile,name='viewprofile'),
	url(r'^groupThread/(?P<username>.+)/(?P<projectname>.+)/$',group_thread,name='groupThread'),
	url(r'^post/(?P<username>.+)/(?P<projectname>.+)/$',add_post,name='addpost'),
	url(r'^friends/decline/(?P<username>.+)/(?P<to_user>.+)/$',user_decline_friend,name='declinefriend'),
	url(r'^friends/accept/(?P<username>.+)/(?P<to_user>.+)/$',user_accept_friend,name='acceptfriend'),
	url(r'^friends/add/(?P<username>.+)/(?P<to_user>.+)/$',user_add_friends,name='addfriend'),
	url(r'^friends/(?P<username>.+)/$',user_fri,name='userfriends'),
	url(r'^(?P<username>.+)/$',user_detail,name='userdetail'),
	url(r'^$',home),
]
