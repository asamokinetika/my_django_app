from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView,LogoutView) 
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from .forms import LoginForm,UserCreateForm
from .models import User
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

