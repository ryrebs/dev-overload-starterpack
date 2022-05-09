from .base import *
from django.urls import path, include
import debug_toolbar

urlpatterns += [
    path("__debug__/", include(debug_toolbar.urls)),
    ## If apps have multiple url's "app_name" named "home"
    ## Django wants to distinguish to what namespace it belongs to.
    path("", include("home.urls", namespace="home")),
]
