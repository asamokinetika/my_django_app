from django.urls import path
from . import views

app_name = 'sns'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/',views.Signup.as_view(),name='signup'),
    path('profile_detail/<int:pk>',views.UserDetail.as_view(),name='profile_detail'),
    path('profile_edit/<int:pk>',views.UserUpdate.as_view(),name="profile_edit"),

]