from django.urls import path
from . import views

app_name = "likes"
urlpatterns = [path("", views.set_like, name="set_like")]

