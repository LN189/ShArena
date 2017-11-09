from __future__ import unicode_literals
from django.forms import ModelForm
import json
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,RegexValidator

##@brief model for allocating rating among users
class rating(models.Model):
    ## rating a user gave to another user(1-5)
    rate = models.CharField(default='5', max_length=1, validators=[RegexValidator(r'^\d{1,10}$')])
    ## The user who is giving the rating
    from_user = models.ForeignKey(User,related_name='from_user')
    ## The user whom he is rating
    to_user =models.ForeignKey(User,related_name='to_user')


##@brief Model for a posting a post in group by the user it caontains the created_time, message, author, title of the message
class post(models.Model):
    ##Title of the post posted by auser in group thread
    title = models.CharField(max_length=200,default="")
    ##The user who posting the post in group thread
    author = models.ForeignKey(User)
    ## Created time of the post
    created_at = models.DateTimeField(auto_now_add=True)
    ##Project of the group thread
    ofProject = models.CharField(max_length=200,default="")
    ##Message in the post
    text = models.TextField()

##@brief form for posting a post in the group thread it contains title, text fields automatically fields defaultly fixed in background
class postingForm(ModelForm):
    ##@brief meta data related to postingForm ModelForm
    class Meta:
        model = post
        fields = {'title','text',}

##@brief Model for a dealing with projectrequest between users
class projectrequest(models.Model):
    ##The user who wanted to join the project
    from_user = models.ForeignKey(User,related_name='fromuser')
    ##The tilte of the project
    to_pro = models.CharField(max_length=200,default="")
