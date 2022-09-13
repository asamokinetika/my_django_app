from dataclasses import InitVar
from pyexpat.errors import messages
from django.shortcuts import render,redirect, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import(LoginView,LogoutView) 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from .forms import LoginForm,UserCreateForm,UserEditForm,FindUserForm,FriendMessageForm
from .models import FriendMessage, User,Friend
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
        users=User.objects.all()
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
    if request.method=="POST":
        form=FriendMessageForm(request.POST)
        owner=request.user
        friend=Friend.objects.get(id=pk)
        receiver=friend.inviter
        content=request.POST['content']
        new_msg=FriendMessage(owner=owner,receiver=receiver,content=content)
        new_msg.save()
        return redirect('sns:talkroom_friend',pk=pk)
    else: 
        form=form=FriendMessageForm()
        friend=Friend.objects.get(id=pk)
        person=friend.inviter
        messages=FriendMessage.objects.filter(Q(owner=request.user,receiver=person)|Q(owner=person,receiver=request.user))
        params={
            'messages':messages,
            'form':form,
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


        new_friend_invitation=Friend(inviter=request.user,invitee=invitee,auth=False)
        new_friend_invitation.save()
        new_friend_invitation2=Friend(inviter=invitee,invitee=request.user,auth=True)
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