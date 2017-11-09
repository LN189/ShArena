from django.conf.urls import url
from .views import group, getgroups, deleting, accepting, send_project, new_project, files_view, upload_file, list_files, add_member, file_view, file_saving, others_view, delete_file, delete_project, upload_pic, file_merge, merge_files, merge_type

urlpatterns = [
	url(r'^(?P<user>.+)/(?P<projectname>.+)/groups/$',send_project,name = 'sendproject'),
	url(r'^(?P<user1>.+)/(?P<username>.+)/(?P<projectname>.+)/accept/$',accepting,name = 'accepting'),
	url(r'^(?P<user1>.+)/(?P<username>.+)/(?P<projectname>.+)/delete/$',deleting,name = 'deleting'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/mergetype/$',merge_type,name='mergetype'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/mergefiles/$',merge_files,name='mergefiles'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/merge/$',file_merge,name = 'merge'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/display/$',file_saving,name='filesaving'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/view/view$',others_view,name='othersfile1'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/view/$',others_view,name='othersfile'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/delete/$',delete_file,name='deletefile'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/add/(?P<to_username>.+)/$',add_member,name='addmember'),
	url(r'^(?P<username>.+)/(?P<project>.+)/new/$',upload_file,name= 'uploadfile'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/deletep/$',delete_project,name= 'deleteproject'),
	url(r'^(?P<mainUser>.+)/(?P<username>.+)/(?P<projectname>.+)/list/$',list_files,name='listfilesofauthor'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/(?P<filename>.+)/$',file_view,name='openfile'),
	url(r'^(?P<username>.+)/new/$',new_project,name = 'newproject'),
	url(r'^(?P<username>.+)/picture/$',upload_pic,name = 'profilepic'),
	url(r'^(?P<username>.+)/(?P<projectname>.+)/$',files_view,name='fileslist'),
	url(r'^(?P<username>.+)/$',getgroups,name='usergroups'),
	url(r'^$',group,name='groups'),
]
