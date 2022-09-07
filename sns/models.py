from cProfile import label
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin,UserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    prof_img=models.ImageField(upload_to='images/')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Group(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='group_owner')
    group_name=models.CharField(max_length=100)

    def __str__(self):
        return str(self.group_name)+'(groupowner:'+str(self.owner)+')'

class Friend(models.Model):
    inviter=models.ForeignKey(User,on_delete=models.CASCADE,related_name='inviter')
    invitee=models.ForeignKey(User,on_delete=models.CASCADE,related_name='invitee')
    auth=models.BooleanField()
    def __str__(self):
        return 'Friend Invitation'+str(self.inviter)+'to'+str(self.invitee)

class GroupInvitation(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='group')
    inviter=models.ForeignKey(User,on_delete=models.CASCADE,related_name='inviter')
    invitee=models.ForeignKey(User,on_delete=models.CASCADE,related_name='invitee')
    auth=models.BooleanField()
    def __str__(self):
        return 'Group Invitation'+str(self.inviter)+'to'+str(self.invitee)

class FriendMessage(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_owner')
    receiver=models.ForeignKey(Friend,on_delete=models.CASCADE,related_name='message_receiver')
    content=models.TextField(max_length=1000)
    pub_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.contents)+'('+str(self.owner)+')'
    class Meta:
        ordering=('-pub_date',)

class GroupMessage(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_owner')
    Group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='message_receiver')
    content=models.TextField(max_length=1000)
    pub_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.contents)+'('+str(self.owner)+')'
    class Meta:
        ordering=('-pub_date',)
