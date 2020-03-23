#slug implementation from a text
from django.db.models.signals import pre_save #signal before save the istance
from django.dispatch import receiver
from django.utils.text import slugify 

from core.utils import generate_random_string 
from events.models import Event

@receiver(pre_save, sender=Event)   #when a signal is triggered  create a slug based on the attribute "title"
def add_slug_to_event(sender, instance, *args, **kwargs): 
    if instance and not instance.slug:
        slug = slugify(instance.title)    #content is the slug text
        random_string = generate_random_string() #to make unique the slug
        instance.slug = slug + "-" + random_string

