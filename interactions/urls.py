from django.urls import path
from . import views
app_name='interactions'
urlpatterns=[path('<slug:slug>/like/',views.like,name='like'),path('<slug:slug>/comment/',views.comment,name='comment')]
