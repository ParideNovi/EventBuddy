from django.urls import path
from users.api.views import CurrentUserAPIView, UserDetailAPIView,UserEventListAPIView,UserEventReviewListAPIView, ProfileDetailAPIView

urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name="current-user"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-details"),
    path("users/<int:pk>/eventsExpired/", UserEventListAPIView.as_view(), name="user-events"),
    path("users/<int:pk>/reviews/", UserEventReviewListAPIView.as_view(), name="user-reviews"),
    path("profiles/<str:user_id__username>/", ProfileDetailAPIView.as_view(), name="profile-details")

]
