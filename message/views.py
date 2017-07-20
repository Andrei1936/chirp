from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from message.forms import RegisterForm
from message.models import Message


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = "/"


class TimelineView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        print(self.request.user.is_authenticated())
        if self.request.user.is_authenticated():
            return Message.objects.filter(user=self.request.user)
        else:
            return Message.objects.all()
