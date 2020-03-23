from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from users.api.serializers import UserDisplaySerializer,ProfileDisplaySerializer,ProfileAvatarSerializer
from rest_framework import  generics 
from events.api.serializer import EventSerializer,ReviewSerializer
from users.models import CustomUser,Profile
from events.models import Event,Review
from users.api.permissions import IsAdminUserOrReadOnly, IsOwnProfileOrReadOnly
from rest_framework.permissions import IsAuthenticated

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
    lookup_field = "user_id__username"     
    serializer_class = EventSerializer
    permission_classes = [ IsAdminUserOrReadOnly]  

    def get_queryset(self):
        kwarg_author = self.kwargs.get("user_id__username")
        return Event.objects.filter(author__username=kwarg_author,expired_event=True).order_by("-created_at")

#list reviews got it from the <pk> User = event__author 
class UserEventReviewListAPIView(generics.ListAPIView): 
    ''' Lista delle reviews fatte allo user(username), cioè l'autore degli eventi '''
    lookup_field = "user_id__username" 
    serializer_class = ReviewSerializer
    permission_classes = [ IsAdminUserOrReadOnly]  
    
    def get_queryset(self):
        kwarg_author = self.kwargs.get("user_id__username") #get kwarg_author_id by the url key "pk"
        return Review.objects.filter(event__author__username=kwarg_author).order_by("-created_at") #the event__author of the reviews is the pk user


#Profile pk Details
class ProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):  
    #specifying the Profile username, it'll match(1:1) with the User user_id.username
    #i need all the details of the Profile model
    ''' Dettagli/Modifica/cancellazione del Profilo(username) <--> User(user_id.username)  "profiles/<str:user_id__username>/" '''
   # kwarg_username 
    lookup_field = "user_id__username"   #use the url field to make the query
    queryset = Profile.objects.all()
    serializer_class = ProfileDisplaySerializer
    permission_classes = [  IsOwnProfileOrReadOnly ]  #SAFE for normal users, Update/destroy for Admin or IsYourProfile


class AvatarUpdateView(generics.UpdateAPIView):         #è piu semplice usare solo gli APIViews
    '''Avatar Profilo, API dedicato '''
                     #use the url field to make the query
    serializer_class = ProfileAvatarSerializer          #
    permission_classes = [IsAuthenticated]              #basta questo senza isOwnerOrReadOnly pechhè sovrascriviamo il metodo get_object

    def get_object(self):                               #sovrascrivendo tale metodo non abbiamo bisogno di passare una chiave primaria nel nostro endpint 
                                                        #vogliamo solo un endpoint API/avatar e lo aggiorniamo sulla base del profilo (loggato) che sta facendo la richiesta
                                                        #farà una put solo sull'avatar(come serializzato) prendendo l'user da se stesso
        profile_object = self.request.user.profile      
        return profile_object                          
