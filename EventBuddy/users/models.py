from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# i'll extend user which eredit from the AbstractUser, istead collegate a profile to user.
class CustomUser(AbstractUser):    #set in settings that we are using User Custom  
    pass
    #bio = models.TextField(max_length=500,null=True, blank=True)
    #location = models.CharField(max_length=100,null=True, blank=True)
    #birth_date = models.DateField(null=True, blank=True)
    #avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    #rating = calculated clientside as average of review(id).rating 


#i made 2 different Models to have registered personalized fields in the admin.py 
class Profile(models.Model):  
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) #relazione 1-1
    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username  #from CustomUser
                            