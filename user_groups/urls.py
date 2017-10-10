from django.conf.urls import url
from .views import group, groups_view, new_project, files_view, upload_file, list_files, add_member, file_view, update_db

urlpatterns = [
	url(r'^(?P<username>.+)/(?P<projectname>.+)/add/(?P<to_username>.+)/$',add_member,name='addmember'),
	url(r'^(?P<username>.+)/(?P<project>.+)/new/$',upload_file,name= 'uploadfile'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/list/$',list_files,name='listfilesofauthor'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/$',file_view,name='openfile'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/(?P<matter>.+)/$',update_db,name='dbupdater'),
	url(r'^(?P<username>.+)/new/$',new_project,name = 'newproject'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/$',files_view,name='fileslist'),
	url(r'^(?P<username>.+)/$',groups_view.as_view(),name='usergroups'),
	url(r'^$',group,name='groups'),
]
