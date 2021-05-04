from django.urls import path
from django.views.generic import TemplateView
from useraccount import views

APP_NAME = 'useraccount'


urlpatterns = [

    path("", views.temphomeview),
    path("home/", views.homeview ,name = 'home' ),

    path("profile/",views.userprofileview , name= "userprofile"),
    path("allusers/",views.allusersview, name= 'allusers'),

    path("findpatient/", views.findpatientview , name = 'findpatient'),
    path("allpatients/", views.allpatientsview , name = 'allpatients'),
    path("patient/<str:id>/",views.patientprofileview , name = 'patientprofile'),

    path("medication/addmed/<str:id>/",views.addmedview , name = 'addmed'),
    path('medication/editmed/<int:pk>/', views.editmedview, name = 'editmed'),
    path('medication/deletemed/<int:pk>/', views.deltemedview, name = 'deletemed'),

]
