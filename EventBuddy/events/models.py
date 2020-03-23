
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator #per il punteggio di un rating

#class based
class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, unique=True) #A "slug" is a way of generating a valid unique URL, generally using data already obtained. 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, #users.CustomUser
                                on_delete=models.CASCADE,
                                related_name="events")
    description = models.CharField(max_length=400)
    start_date = models.DateTimeField()
    location = models.CharField(max_length=120) #città
    picture = models.ImageField(blank=True,null=True) 
    price = models.FloatField(blank=True,default=0)
    #group_components = models.CharField(blank=true) #lista di users che aderiscono, sommati<group_limit
    group_limit = models.IntegerField(default=1)
    expired_event = models.BooleanField(default=False)

    def __str__(self):
        return f" { self.title } "

class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body   = models.TextField(blank=True, null=True)
    event = models.ForeignKey(Event,                        #the event of the review
                            on_delete = models.CASCADE,
                            related_name="reviews")         #le reviews di quell'evento(pk)    
    author = models.ForeignKey(settings.AUTH_USER_MODEL,            #user(pk) which writes the review
                                    on_delete = models.CASCADE)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,       #the review can be voted from many(pk) 
                                    related_name="votes")                                      
    rating = models.PositiveIntegerField(validators =[MinValueValidator(1), #the single vote(1-5) of the review about the Event
                                                        MaxValueValidator(5)])                                
    

    def __str__(self):
        return f" { self.author.username , str(self.rating)} "
 
        
