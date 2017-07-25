from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.db.utils import IntegrityError

from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from message.forms import RegisterForm
from message.models import Message, Follow


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = "/login"

class TimelineView(ListView):
    template_name = 'index.html'
    def get_queryset(self):
        # implement the logic
        if self.request.user.is_authenticated:
            return Message.objects.filter(user=self.request.user)
        else:
            return Message.objects.all()

class ProfileBaseView(DetailView):
    model = User
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileBaseView, self).get_context_data(**kwargs)
        context["chirps"] = Message.objects.filter(user=self.get_object())
        following = Follow.objects.filter(following_user=self.request.user)
        context["following"] = [f.followed_user for f in following]
        followers = Follow.objects.filter(followed_user=self.request.user)
        context["followers"] = [f.following_user for f in following]
        return context

class MyProfileView(ProfileBaseView):
    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(ProfileBaseView):
    def get_slug_field(self):
        return "username"


def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    try:
        follow = Follow(followed_user=user, following_user=request.user)
        follow.save()
        messages.info(request, "You are now following {0}".format(username))
    except IntegrityError:
        messages.error(request, "You are already following this user")
        return redirect('profile', username)