from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('home/', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('', views.login_user, name="login_user"), 
    path('logout_user/', views.logout_user, name='logout_user'),

 
    path('admin/', views.admin, name='admin'),  
    path('adminpanel/', views.adminpanel, name="adminpanel"),  
    path('searchuser/', views.searchuser, name="searchuser"),  
    path('update/<str:username>/',edit,name='update'),
    path('delete/<str:username>/',delete,name='delete'),
]
