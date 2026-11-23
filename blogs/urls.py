from django.urls import path
from . import views
app_name='blogs'
urlpatterns=[path('',views.listing,name='list'),path('mine/',views.mine,name='mine'),path('new/',views.create,name='create'),path('<int:pk>/edit/',views.edit,name='edit'),path('<int:pk>/delete/',views.delete,name='delete'),path('<slug:slug>/',views.detail,name='detail')]
