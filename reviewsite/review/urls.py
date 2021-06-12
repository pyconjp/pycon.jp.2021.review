from django.urls import path

from . import views

app_name = "review"
urlpatterns = [
    path("proposal/", views.list_proposals, name="list_proposals"),
]
