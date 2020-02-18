from django.urls import path
from users.api.views import (CurrentUserAPIView, UserDetailAPIView,UserEventListAPIView,
                            UserEventReviewListAPIView, ProfileDetailAPIView,AvatarUpdateView)

urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name="current-user"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-details"),
    path("profiles/<str:user_id__username>/eventsExpired/", UserEventListAPIView.as_view(), name="user-events"),
    path("profiles/<str:user_id__username>/reviews/", UserEventReviewListAPIView.as_view(), name="user-reviews"),
    path("profiles/<str:user_id__username>/", ProfileDetailAPIView.as_view(), name="profile-details"),
    path("profiles/<str:user_id__username>/avatar/", AvatarUpdateView.as_view(), name="avatar-update") #dedicated API
]



#with routers 05_DRF_LV_3

