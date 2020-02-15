from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from users.api.serializers import UserDisplaySerializer,ProfileDisplaySerializer
from rest_framework import  generics 
from events.api.serializer import EventSerializer,ReviewSerializer
from users.models import CustomUser,Profile
from events.models import Event,Review
from users.api.permissions import IsAdminUserOrReadOnly, IsOwnProfileOrReadOnly

#class APIView get user (ourself)
class CurrentUserAPIView(APIView):
    ''' Dettagli dello user loggato '''
    def get(self, request):
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data) #username

#user pk Details
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):  
    ''' Dettagli dello user(pk) '''
    queryset = CustomUser.objects.all()
    serializer_class = UserDisplaySerializer
    permission_classes = [ IsAdminUserOrReadOnly]  #SAFE for normal users, Update/destroy for Admin
    
#list events of tha <pk> User = event.author_id 
class UserEventListAPIView(generics.ListAPIView): 
    ''' Lista degli eventi organizzati dallo user(pk), cioè l'autore degli eventi '''    
    serializer_class = EventSerializer
    permission_classes = [ IsAdminUserOrReadOnly]  

    def get_queryset(self):
        kwarg_author_id = self.kwargs.get("pk")
        return Event.objects.filter(author=kwarg_author_id,expired_event=True).order_by("-created_at")

#list reviews got it from the <pk> User = event__author 
class UserEventReviewListAPIView(generics.ListAPIView): 
    ''' Lista delle reviews fatte allo user(pk), cioè l'autore degli eventi '''
    serializer_class = ReviewSerializer
    permission_classes = [ IsAdminUserOrReadOnly]  
    
    def get_queryset(self):
        kwarg_author_id = self.kwargs.get("pk") #get kwarg_author_id by the url key "pk"
        return Review.objects.filter(event__author=kwarg_author_id).order_by("-created_at") #the event__author of the reviews is the pk user


#Profile pk Details
class ProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):  
    #specifying the Profile username, it'll match(1:1) with the User user_id.username
    #i need all the details of the Profile model
    ''' Dettagli del Profilo(username) <--> User(user_id.username)  "profiles/<str:user_id__username>/" '''
   # kwarg_username 
    lookup_field = "user_id__username"   #use the url field to make the query
    queryset = Profile.objects.all()
    serializer_class = ProfileDisplaySerializer
    permission_classes = [  IsOwnProfileOrReadOnly ]  #SAFE for normal users, Update/destroy for Admin or IsYourProfile

