from django.urls import path

from . import views

app_name = "apiv1"
urlpatterns = [
    path("proposals/", views.ProposalCreateAPIView.as_view()),
]
