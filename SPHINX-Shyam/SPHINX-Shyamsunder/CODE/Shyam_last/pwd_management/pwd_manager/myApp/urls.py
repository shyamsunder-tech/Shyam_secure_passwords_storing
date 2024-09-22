from django.urls import path
from .views import myView
urlpatterns = [
    path("", myView, name="myView"),
]