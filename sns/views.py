from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView,LogoutView) 
from django.views import generic
from.forms import LoginForm
# Create your views here.
class Top(generic.TemplateView):
    template_name ='sns/top.html'

class Login(LoginView):
    form_class = LoginForm
    template_name ='sns/login_form.html'

class Logout(LogoutView):
    template_name='sns/top.html'

