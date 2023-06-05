from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=2000,null=True,unique=True)

    def __str__(self) -> str:
        return self.username

state = (('rapid api data initilized','rapid api data initilized'),
         ('scrapper data initilized','scrapper data initilized'),
         )

class profile(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    username = models.CharField(max_length=1000,null=True,unique=True)
    region = models.CharField(max_length=10000,null=True,blank=True)
   
    followers_count = models.CharField(max_length=10000,null=True,blank=True)
    following_count = models.CharField(null=True,max_length=100000,blank=True)

    likes = models.CharField(max_length=100000,null=True,blank=True)
    signature = models.CharField(max_length=100000,null=True,blank=True)
    
    profile_photo_url = models.CharField(max_length=100000,null=True,blank=True)
    
    videos = models.TextField(null=True,blank=True) # JSON-serialized (text) version of your list
    email = models.CharField(null=True,max_length=1000,blank=True)
    all_feild_status = models.BooleanField(default=False,null=True) # have the all feild?
    #state = models.CharField(choices=state,null=True,max_length=1000)

    uid = models.CharField(null=True,unique=True,max_length=10000)
    category = models.CharField(null=True,max_length=10000,blank=True)

    def __str__(self):
        return self.username

    #return self.user.username

class Follower(models.Model):
    uid = models.CharField(null=True,max_length=10000)
    username  = models.CharField(null=True,max_length=10000) ## not unique 
    influencer = models.ForeignKey(profile,on_delete=models.SET_NULL,null=True,max_length=10000)
    region = models.CharField(null=True,max_length=10000)
    profile_photo = models.CharField(null=True,max_length=100000)
    age = models.IntegerField(null=True)
    signature = models.CharField(null=True,max_length=100000)
    email = models.CharField(null=True,max_length=10000)
    likes = models.CharField(null=True,max_length=100000)
    follower_count = models.CharField(null=True,max_length=100000)
    following_count = models.CharField(null=True,max_length=100000)
    
    def __str__(self):
        return self.username
    

class api_call(models.Model):
    count = models.IntegerField(null=True)
    
space = "RAM==BHAGWAN"



