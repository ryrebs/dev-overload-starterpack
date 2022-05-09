from django.urls import path

from . import views

## For accessing reverse url: home:index
app_name = "home"

urlpatterns = [path("", views.index, name="index")]
