from django.urls import path

from . import views

app_name = "apiv1"
urlpatterns = [
    path("proposals/", views.ProposalCreateAPIView.as_view()),
    path("proposals/scores/", views.ProposalReviewScoreListAPIView.as_view()),
    path("reviews/", views.ReviewListAPIView.as_view()),
]
