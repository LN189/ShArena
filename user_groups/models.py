from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
user=''
pro=''
blah=''
class project(models.Model):
	title = models.CharField(max_length=200,default="")
	authors = models.ManyToManyField(User)

	def __str__(self):
		return self.title
	# Create your models here.

class projectform(ModelForm):
	class Meta:
		model = project
		fields = '__all__'
def user_directory_path():
	direc = user+'/'+pro+'/'
	print(direc) 
	return direc

class textfile(models.Model):
	title = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to=blah)
	uploaded_at = models.DateTimeField(auto_now_add=True)
class textfileForm(ModelForm):
	def __init__(self,*args,**kwargs):

		user=kwargs.pop('user',None)
		user=str(user)
		pro=kwargs.pop('pro',None)
		pro=str(pro)
		blah=user+"/"+pro+"/"
		print(blah)
		super(textfileForm,self).__init__(*args,**kwargs)
	class Meta:
		model = textfile
		fields = ('title', 'document')

