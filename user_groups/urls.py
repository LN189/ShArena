from django.conf.urls import url
from .views import group, groups_view, new_project, files_view

urlpatterns = [
	url(r'^(?P<username>.+)/new/$',new_project,name = 'newproject'),
	#url(r'^(?P<username>.+)/(?P<project>.+)/new/$',upload_file,name= 'uploadfile'),
	url(r'^(?P<username>.+)/(?P<project>.+)/$',files_view,name='fileslist'),
	url(r'^(?P<username>.+)/$',groups_view.as_view(),name='usergroups'),
	url(r'^$',group,name='groups'),
]