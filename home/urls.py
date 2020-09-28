from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [

    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),


    path('', views.dashboard, name='dashboard'),  
    path('userPage', views.userPage, name='userPage'),
    path('medications', views.medications, name='medications'),
    path('patient/<str:pk_test>', views.patient, name='patient'),
    path('statistics', views.statistics, name='statistics'),
    path('account_settings', views.account_settings, name='account_settings'),


    path('createAppoinment/<str:pk>', views.createAppoinment, name='createAppoinment'),
    path('updateAppoinment/<str:pk>', views.updateAppoinment, name='updateAppoinment'),
    path('deleteAppoinment/<str:pk>', views.deleteAppoinment, name='deleteAppoinment'),


]
