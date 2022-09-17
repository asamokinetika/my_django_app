
from dataclasses import field
from django import forms
from .models import User
from django.contrib.auth.forms import (
    AuthenticationForm,UserCreationForm
)


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
    
class UserCreateForm(UserCreationForm):
    class Meta:
        model=User
        fields=["email","name","password1","password2"]

    
class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('name','img')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'    

class FindUserForm(forms.Form):
    find=forms.CharField(label='ユーザー名前検索',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))



class FriendMessageForm(forms.Form):
    content=forms.CharField(max_length=1000)



class CreateGroupForm(forms.Form):
    def __init__(self,user,friends=[],vals=[],*args,**Kwargs):
        super(CreateGroupForm,self).__init__(*args,**Kwargs)
        self.fields['room_name']=forms.CharField(label='room_name',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['friends']=forms.MultipleChoiceField(
            choices=[(item.inviter.id,item.inviter.name) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals
        )
        self.fields['img']=forms.ImageField(label='img',)
