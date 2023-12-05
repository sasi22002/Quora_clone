from django.urls import path
from masteradmin import views


urlpatterns = [
    path('my_profile',views.Myprofile.as_view(),name='my_profile'),

       
    ]
    