from .base import *
from django.urls import path, include

urlpatterns += [
    ## If apps have multiple url's "app_name" named "home"
    ## Django wants to distinguish to what namespace it belongs to.
    path("", include("home.urls", namespace="home")),
]
