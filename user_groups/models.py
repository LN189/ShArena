from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django import forms
import os

## @brief Model for representing a project
class project(models.Model):
	## Title for the project
	title = models.CharField(max_length=200,default="",unique=True)
	## Members associated with the project
	authors = models.ManyToManyField(User)
	## A short description of project of minimum 50 words
	description = models.TextField(max_length=500,default="")
	##Informal string representation of the project model
	def __str__(self):
		return self.title

## @brief Form for creating the model project
class projectform(ModelForm):
	description = forms.CharField(max_length=500, min_length=50)
	class Meta:
		model = project
		fields = '__all__' #forms contains all fields

## @brief Function to specify the path for the file in database where it should be stored
def user_directory_path(instance,filename):
	##  name path of the file in the database user_username/project/filename
	name='user_{0}/{1}/{2}'.format(instance.user.username,instance.pro,filename)
	print(filename)
	if os.path.exists('media/'+name):
		os.remove('media/'+name)
		return name
	else:
		return name

## @brief function for the path of the profile pic of the users in the database
def user_image_path(instance,filename):
	## @param path of profilepic admin_images/username/imagename
	nameimage = 'admin_images/{0}.{1}'.format(instance.user.username,"jpg")
	if os.path.exists('media/'+nameimage):
		prev = get_object_or_404(profilePicture,title=instance.user.username).delete()
		os.remove('media/'+nameimage)
		return nameimage
	else:
		return nameimage

## @brief Model for representing the file uses ::user_directory_path function for uploading path od file in database
class textfile(models.Model):
	## title for the file
	title = models.CharField(max_length=255, blank=True)
	## File uploaded user
	user = models.ForeignKey(User)
	## project of uploaded file
	pro = models.CharField(max_length=255, blank=True)
	## field for storing the data in file
	document = models.FileField(upload_to=user_directory_path) #
	## uploaded time of file
	uploaded_at = models.DateTimeField(auto_now_add=True) # time at which the file os uploaded

## @brief Form for uploading the new file it contains only title and document field , the remaning fields are fixed by default in background
class textfileForm(ModelForm):
    class Meta:
        model = textfile
        fields = ('title', 'document')

## @brief Model for the profile pic of the user, uses user_image_path for uploading the image in respective path in database
class profilePicture(models.Model):
	##Title of the profile pic
	title = models.CharField(max_length=255, blank=True)
	##Logged in User
	user = models.ForeignKey(User)
	##Field for storing profilepic
	pic = models.ImageField(upload_to=user_image_path)

## @brief Modleform for uploading the profile pic
class profilePicForm(ModelForm):
	##meta data of the profilePicForm ModelForm
	class Meta:
		model = profilePicture
		fields = ('pic',)

## @brief Model that represents the merge_rewuests
class merge_requests(models.Model):
	## Title for the merging part of code
	title = models.CharField(max_length=100)
	## To the user the code is being sent
	to_user =  models.ForeignKey(User,related_name='to_userMerge')
	## Name of the file to which the code is to be merged
	filename = models.CharField(max_length=100)
	## From the user code is being sent
	from_user = models.ForeignKey(User,related_name='from_userMerge')
	## field that stores sending code
	data = models.TextField(max_length=10000000000)

	##meta data of the merge_requests model
	class Meta:
		unique_together = ["from_user" , "to_user" , "data" , "title" , "filename"]

	## informal string representation of merge_requests model
	def __str__(self):
		return "User #%s send a merge request " % (self.from_user.username)
