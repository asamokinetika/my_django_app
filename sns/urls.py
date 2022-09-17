from django.urls import path

from sns.models import Friend
from . import views

app_name = 'sns'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/',views.Signup.as_view(),name='signup'),
    path('profile_detail/<int:pk>',views.UserDetail.as_view(),name='profile_detail'),
    path('profile_edit/<int:pk>',views.UserUpdate.as_view(),name="profile_edit"),
    path('hello/',views.hello,name="hello"),
    path('user_list',views.UserList,name="user_list"),

    path('friend_list',views.FriendList,name="friend_list"),
    path('talkroom_friend/<int:pk>',views.Friendtalk,name="talkroom_friend"),
    path('friend_request/<int:pk>',views.FriendRequest,name="friend_request"),
    path('friend_request_accept/<int:pk>',views.FriendRequestAccept,name='friend_request_accept'),

    path('group_list',views.GroupList,name='group_list'),
    path('talkroom_group/<int:pk>',views.Grouptalk,name="talkroom_group"),
    path('create_group',views.CreateGroup,name='create_group'),
    path('group_request_accept/<int:pk>',views.GroupRequestAccept,name='group_request_accept'),
    
    path('base', views.base, name='top'),

]