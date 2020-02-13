import locale
import datetime
from rest_framework import serializers
from events.models import Review, Event

from django.utils.timesince import timeuntil,timesince

locale.setlocale(locale.LC_ALL, 'it_IT.utf8') #transalte the date

class ReviewSerializer(serializers.ModelSerializer):
    #event = serializers.StringRelatedField(read_only=True) #every Review shows the event.title NOPE!! 
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    #has_been_modified = serializers.SerializerMethodField(read_only=True) 
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True) #if the user already liked the review
    event_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        exclude = ["event","voters", "updated_at"] #exclude what i don't need

    def get_created_at(self, instance):
        return instance.created_at.strftime('%d %B %Y') #format day month year

    def get_likes_count(self, instance):
        return instance.voters.count()              #count all the voters

    def get_user_has_voted(self, instance):
        request = self.context.get("request")          #request get to the API 
        return instance.voters.filter(pk=request.user.pk).exists() #True if exist my_pk(user.pk) in the voters list

    def get_event_slug(self, instance):
        return instance.event.slug

class EventSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    reviews_count = serializers.SerializerMethodField(read_only=True)
    expired_event = serializers.SerializerMethodField(read_only=True)  # date_now < start_date
    user_has_reviewed = serializers.SerializerMethodField(read_only=True) #a user can't reviewed his event
    #group_is_full = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Event
        exclude = ["updated_at"]

    def get_reviews_count(self, instance):
        return instance.reviews.count()

    def get_created_at(self, instance):
        return instance.created_at.strftime('%d %B %Y')

    def get_user_has_reviewed(self, instance): #true also if 
        request = self.context.get("request")
        has_reviewed = instance.reviews.filter(author=request.user).exists()
        return has_reviewed

    '''def get_group_is_full(self, instance):
        # request = self.context.get("request")
        return group_components.count() <= group_limit'''        

    def get_expired_event(self, instance): #check if the event is expired
        start_date = instance.start_date
        time_delta = timeuntil(start_date) #even if it is a string, i can't compare it..
        time_zero = timesince(start_date,start_date) 
        return time_delta == time_zero
        