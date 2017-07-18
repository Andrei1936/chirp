from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView

from message.forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = "/"