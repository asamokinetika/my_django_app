from dataclasses import InitVar, field
from pyexpat.errors import messages
from django.shortcuts import render,redirect, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import(LoginView,LogoutView) 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from .forms import  LoginForm,UserCreateForm,UserEditForm,FindUserForm,FriendMessageForm,CreateGroupForm
from .models import FriendMessage, TalkRoom, User,Friend,Group,GroupInvitation,GroupMessage
from django.db.models import Q
from django.urls import reverse_lazy

# Create your views here.
class Top(generic.TemplateView):
    template_name ='sns/top.html'

class Login(LoginView):
    form_class = LoginForm
    template_name ='sns/login_form.html'

class Logout(LogoutView):
    template_name='sns/top.html'

class Signup(CreateView):
    form_class=UserCreateForm
    template_name="sns/signup.html"
    success_url=reverse_lazy("sns:top")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'sns/profile_detail.html'


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'sns/profile_edit.html'

    def get_success_url(self):
        return resolve_url('sns:profile_detail', pk=self.kwargs['pk'])

@login_required(login_url="sns/login")
def UserList(request):
    if request.method=="POST":
        form=FindUserForm(request.POST)
        find=request.POST['find']
        users=User.objects.filter(name=find)
    else:
        users_friends=Friend.objects.filter(inviter=request.user)
        users_friends_list=[]
        users_friends_list.append(request.user.id)
        for user_friend in users_friends:
            users_friends_list.append(user_friend.invitee.id)
        users=User.objects.exclude(id__in=users_friends_list)
        form=FindUserForm()

    
    params={
        'users':users,
        'form':form,
    }
    return render(request,'sns/user_list.html',params)

#Friend登録、メッセージ機能など
@login_required(login_url="sns/login")
def FriendList(request):
    all_friend=Friend.objects.filter(invitee=request.user,auth=True)
    friend_invitation=Friend.objects.filter(invitee=request.user,auth=False)
    your_invitation=Friend.objects.filter(inviter=request.user,auth=False)
    params={
        'all_friend':all_friend,
        'friend_invitation':friend_invitation,
        'your_invitation':your_invitation,
    }
    return render(request,"sns/friend_list.html",params)

@login_required(login_url="sns/login")
def Friendtalk(request,pk):
    
    
    friend=Friend.objects.get(id=pk)
    talkroom=friend.room
    messages=FriendMessage.objects.filter(room=talkroom).order_by('pub_date')
    params={
            'messages':messages,
            'room':str(talkroom.id),
            'pk':pk
    }
    return render(request,"sns/talkroom_friend.html",params)



@login_required(login_url="sns/login")
def FriendRequest(request,pk):

    if request.method=='POST':
        invitee=User.objects.get(id=pk)
        if invitee==request.user:
            messages.info(request,"自分自身はフレンド申請できません")
            return redirect(to='sns:user_list')
        
        frd_num=Friend.objects.filter(Q(inviter=request.user,invitee=invitee)|Q(inviter=invitee,invitee=request.user)).count()
        if frd_num>0:
            messages.info(request,"フレンド申請済み、もしくはこのユーザーからのフレンド申請を受け取っています")
            return redirect(to='sns:user_list')
        new_talk_room=TalkRoom(name="{}AND{}_friend_talkroom".format(request.user.name,invitee.name))
        new_talk_room.save()

        new_friend_invitation=Friend(inviter=request.user,invitee=invitee,room=new_talk_room,auth=False)
        new_friend_invitation.save()
        new_friend_invitation2=Friend(inviter=invitee,invitee=request.user,room=new_talk_room,auth=True)
        new_friend_invitation2.save()
        return redirect(to='sns:friend_list')
    else:
        params={
            "pk":pk,
            
        }
        return render(request,'sns/friend_request.html',params)
        
@login_required(login_url="sns/login")
def FriendRequestAccept(request,pk):
    if request.method=='POST':
        invitaton=Friend.objects.get(id=pk)
        invitaton.auth=True
        invitaton.save()
        return redirect(to='sns:friend_list')
    else:
        params={
            "pk":pk,
            
        }
        return render(request,'sns/friend_request_accept.html',params)

#グループ機能
@login_required(login_url="sns/login")
def GroupList(request):
    my_group=GroupInvitation.objects.filter(invitee=request.user,auth=True)
    group_invitation=GroupInvitation.objects.filter(invitee=request.user,auth=False)
    
    params={
        'my_group':my_group,
        'group_invitation':group_invitation,
    }
    return render(request,"sns/group_list.html",params)

@login_required(login_url="sns/login")
def CreateGroup(request):
    all_friend=Friend.objects.filter(invitee=request.user,auth=True)
    if request.method=='POST':
        
        new_room=TalkRoom()
        new_room.name=request.POST['room_name']
        new_room.save()
        new_group=Group()
        new_group.owner=request.user
        new_group.group_name=request.POST['room_name']
        new_group.room=new_room
        new_group.save()
        sel_fds=request.POST.getlist('friends')
        sel_user=User.objects.filter(id__in=sel_fds)
        for friend in sel_user:
            new_invitation=GroupInvitation()
            new_invitation.group=new_group
            new_invitation.inviter=request.user
            new_invitation.invitee=friend
            new_invitation.auth=False
            new_invitation.save()
        new_invitation=GroupInvitation()
        new_invitation.group=new_group
        new_invitation.inviter=request.user
        new_invitation.invitee=request.user
        new_invitation.auth=True
        new_invitation.save()
        creategroupform=CreateGroupForm(request.user,friends=all_friend,vals=[])

        return redirect(to='sns:group_list')
    else:
        creategroupform=CreateGroupForm(request.user,friends=all_friend,vals=[])
        
    params={
        'create_form':creategroupform
    }
    return render(request,'sns/create_group.html',params)

@login_required(login_url="sns/login")
def GroupRequestAccept(request,pk):
    if request.method=='POST':
        invitaton=GroupInvitation.objects.get(id=pk)
        invitaton.auth=True
        invitaton.save()
        return redirect(to='sns:group_list')
    else:
        params={
            "pk":pk,
            
        }
        return render(request,'sns/group_request_accept.html',params)



@login_required(login_url="sns/login")
def Grouptalk(request,pk):
    
    
    Groupinvi=GroupInvitation.objects.get(id=pk)
    group=Groupinvi.group
    group_name=Groupinvi.group.group_name
    talkroom=group.room
    messages=GroupMessage.objects.filter(Group=group).order_by('pub_date')
    params={
            'messages':messages,
            'room':str(talkroom.id),
            'pk':pk,
            'group_name':group_name
    }
    return render(request,"sns/talkroom_group.html",params)

def base(request):
    return render(request,"sns/base.html")