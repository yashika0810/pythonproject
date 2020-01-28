from django.conf.urls import url
from django.urls import path
from . import views

#app_name = 'myapp'
urlpatterns = [
    url(r'^$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
   # path('delete/<int:id>', views.user_delete, name='user_delete'),
    path('login/', views.logindetails, name='logindetails'),
    path('welcomee/', views.welcomee, name='welcomee'),
    path('myapp/delete/<int:id>', views.delete, name='delete_detail'),
    path('api/', views.LoginMemberAPI.as_view(), name='json'),

    
 
   
]