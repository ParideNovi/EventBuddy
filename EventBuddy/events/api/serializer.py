import locale
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
        if request is None:
            return False        
        return instance.voters.filter(pk=request.user.pk).exists() #True if exist my_pk(user.pk) in the voters list

    def get_event_slug(self, instance):
        return instance.event.slug

class EventSerializer(serializers.ModelSerializer):  
    # ModelSerializer has auto create()/update(), it needs only the "not simple" attributes 
    # with their def get_sttribute, if i need to save in the Model(db istance),
    # do instance.attribute = value     instance.save()  example: def get_expired_event
 
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
        if request is None:
            return False
        has_reviewed = instance.reviews.filter(author=request.user).exists()
        return has_reviewed    

    def get_expired_event(self, instance): #check if the event is expired
        start_date = instance.start_date
        time_delta = timeuntil(start_date) #even if it is a string, i can't compare it..
        time_zero = timesince(start_date,start_date) 
        instance.expired_event = time_delta == time_zero# validated_data.get(True, instance.expired_event)
        instance.save()
        return time_delta == time_zero
         

class EventPictureSerializer(serializers.ModelSerializer): #Modelserializer specifico Avatar tramite singolo endpoit di tipo formdata (non Json)! 
 # in questo caso senza ModelViewSet apposito meglio usare delle generic APIview con i ViewSets nel file views.py
    class Meta:                           
        model = Event
        fields = ["picture"]   #permette di modificare solo gli avatar #vedi views.url


''' def get_group_is_full(self, instance):
        # request = self.context.get("request")
        return group_components.count() <= group_limit'''

