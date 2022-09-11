from django.shortcuts import render,redirect, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import(LoginView,LogoutView) 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from .forms import LoginForm,UserCreateForm,UserEditForm
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