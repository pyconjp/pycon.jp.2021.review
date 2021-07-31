from django.urls import path

from . import views

app_name = "review"
urlpatterns = [
    path("proposal/", views.list_proposals, name="list_proposals"),
    path(
        "proposal/<int:sessionize_id>/",
        views.detail_proposal,
        name="detail_proposal",
    ),
    path("review/", views.list_reviews, name="list_reviews"),
]
