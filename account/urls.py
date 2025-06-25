from django.urls import path

from . import views

app_name="account"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.loginview, name='loginpage'), 
    path('logout/', views.logout_view, name='logoutpage'),
    path('register/', views.registerview, name='registerpage'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/', views.profile_detail, name='profile_detail'),
]
 