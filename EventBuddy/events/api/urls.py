from django.urls import include, path
from rest_framework.routers import DefaultRouter
from events.api import views as ev

router = DefaultRouter() #initialized
router.register(r"events", ev.EventViewSet) 

urlpatterns = [
    path("", include(router.urls)), #endpoint ModelViewSet list /events/ and detail /events/slug/ ""     

    path("events/<slug:slug>/review/",
         ev.ReviewCreateAPIView.as_view(),
         name="create-review"),

    path("events/<slug:slug>/reviews/",
         ev.EventReviewListAPIView.as_view(),
         name="event-review-list"),

    path("reviews/<int:pk>/",
         ev.ReviewRUDAPIView.as_view(),
         name="review-detail"),

    path("reviews/<int:pk>/like/",
         ev.ReviewLikeAPIView.as_view(),
         name="review-like"),

    path("eventsexpired/",
         ev.EventExpiredListAPIView.as_view(),
         name="event-expired-list"),

    path("eventsactive/",
         ev.EventActiveListAPIView.as_view(),
         name="event-active-list"),

path("events/<slug:slug>/picture/",
     ev.PictureUpdateView.as_view(),
     name="picture-update") #dedicated API

]

