from django.shortcuts import get_object_or_404

from rest_framework import generics, status,viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event, Review
from events.api.serializer import EventSerializer, ReviewSerializer
from events.api.permissions import IsAuthorOrReadOnly


class  EventViewSet(viewsets.ModelViewSet): #model gives Get,Post,delete... all of the list 
    ''' Modello lista eventi [IsAuthorOrReadOnly] con dettagli in /slug/'''
    queryset = Event.objects.all().order_by("start_date")
    lookup_field = "slug"  # the queryset id parameter from the url
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EventReviewListAPIView(generics.ListAPIView): #list Event Review (GET)
    ''' Lista degli recensioni dell'evento(slug) ''' 
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Review.objects.filter(event__slug=kwarg_slug).order_by("-created_at")

class ReviewCreateAPIView(generics.CreateAPIView): #create POST Review
    ''' POST creazione review dell' evento(slug) '''
    queryset = Event.objects.filter(expired_event=True)
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        event = get_object_or_404(Event, slug =kwarg_slug)
        #already reviewed
        if event.reviews.filter(author=request_user):   
            raise ValidationError("hai già recensito questo evento! ")
        if event.expired_event == False:   
            raise ValidationError(" non puoi recensire questo evento, non è ancora terminato ! ")
        serializer.save(author=request_user, event=event)


class ReviewLikeAPIView(APIView):
    ''' delete e POST creazione di un like ad una review(pk) '''
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk): #delete a like from a review
        review = get_object_or_404(Review, pk=pk)
        user = self.request.user    #our user making request

        review.voters.remove(user) 
        review.save()
        #using also the serializer                                            
        serializer_context = {"request": request}
        serializer = self.serializer_class(review, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk): #add a like to a review, if you did not do it yet 
        review = get_object_or_404(Review, pk=pk)
        user = self.request.user

        review.voters.add(user)
        review.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(review, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewRUDAPIView(generics.RetrieveUpdateDestroyAPIView):  #Update, Destroy.. Review
    ''' Lista degli recensioni e modifica [IsAuthorOrReadOnly]  '''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

