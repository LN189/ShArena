from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm


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

def user_directory_path(instance,filename):
	return 'user_{0}/{1}/{2}'.format(instance.user.username,instance.pro,filename)

class textfile(models.Model):
	title = models.CharField(max_length=255, blank=True)
	user = models.ForeignKey(User)
	pro = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to=user_directory_path)
	uploaded_at = models.DateTimeField(auto_now_add=True)

class textfileForm(ModelForm):
    class Meta:
        model = textfile
        fields = ('title', 'document')
    #def __init__(self,*args,**kwargs):
    #	self.user=kwargs.pop('user',None)
    #	return super(textfileForm,self).__init__(*args,**kwargs)
    	
    	

	
