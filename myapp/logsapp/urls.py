from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import overviewpage, addprojectpage, loginpage, logoutuser, projectoverviewpage, downloadpage, AddLogsViews, UserViews

#from defender.decorators import watch_login

urlpatterns = [
    path('', csrf_exempt(addprojectpage), name='addprojectpage'),
    path('overview/', csrf_exempt(overviewpage), name='overviewpage'),
    path('addproject/', csrf_exempt(addprojectpage), name='addprojectpage'),
    path('projects-overview/', csrf_exempt(projectoverviewpage), name='projectoverviewpage'),
    path('overview/download/', csrf_exempt(downloadpage), name='downloadpage'),
    path('login/', loginpage, name='loginpage'),
    path('logout/', logoutuser, name='logoutuser'),
    path('addlogs/', csrf_exempt(AddLogsViews.as_view())),
    path('users/', UserViews.as_view())
]
