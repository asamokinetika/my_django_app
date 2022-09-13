
from dataclasses import field
from django import forms
from .models import User
from django.contrib.auth.forms import (
    AuthenticationForm,UserCreationForm
)


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

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
    find=forms.CharField(label='Find',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))



class FriendMessageForm(forms.Form):
    content=forms.CharField(max_length=1000)

"""class FriendListForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super(FriendListForm,self).__init__(*args,**kwargs)
        self.fields['friend_name']=forms. 
"""