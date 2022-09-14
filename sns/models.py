from cProfile import label
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.

def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['image', str(instance.email)+'_'+str(instance.name)+str(".")+str(ext)])

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    name=models.CharField(max_length=50)
    img = models.ImageField(blank=True, null=True, upload_to=upload_path)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

class TalkRoom(models.Model):
    name=models.CharField(max_length=500)
    pub_date=models.DateTimeField(auto_now_add=True)

class Group(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='group_owner')
    group_name=models.CharField(max_length=100)
    room=models.ForeignKey(TalkRoom,on_delete=models.CASCADE,related_name='talk_room_group')

    def __str__(self):
        return str(self.group_name)+'(groupowner:'+str(self.owner)+')'

class Friend(models.Model):
    inviter=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='inviter_friend')
    invitee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='invitee_friend')
    auth=models.BooleanField()
    room=models.ForeignKey(TalkRoom,on_delete=models.CASCADE,related_name='talk_room_friend')
    def __str__(self):
        return 'FriendInvitation '+str(self.inviter)+'_to_'+str(self.invitee)

class GroupInvitation(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='group')
    inviter=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='inviter_group')
    invitee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='invitee_group')
    auth=models.BooleanField()
    def __str__(self):
        return 'GroupInvitation '+str(self.inviter)+'_to_'+str(self.invitee)

class FriendMessage(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='message_owner_friend')
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='message_receiver_friend')
    room=models.ForeignKey(TalkRoom,on_delete=models.CASCADE,related_name='talk_room_friend_message')
    content=models.TextField(max_length=1000)
    pub_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)+'('+str(self.owner)+')'
    class Meta:
        ordering=('-pub_date',)

class GroupMessage(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='message_owner_group')
    Group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='message_receiver_group')
    content=models.TextField(max_length=1000)
    pub_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)+'('+str(self.owner)+')'
    class Meta:
        ordering=('-pub_date',)
