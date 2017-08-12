from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from message.forms import RegisterForm, MessageForm
from message.models import Message, Follow, Like


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = "/login"

class TimelineView(ListView):
    template_name = 'index.html'
    def get_queryset(self):
        #return Message.objects.all().order_by("-created")
        #implement the logic
        if self.request.user.is_authenticated:
            #return Message.objects.filter(user=self.request.user).order_by("-created")
        #else:
            return Message.objects.all().order_by("-created")

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

def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    try:
        follow = Follow.objects.filter(followed_user=user, following_user=request.user).first()
        follow.delete()
        messages.info(request, "You are no longer following {0}".format(username))
    except IntegrityError:
        messages.error(request, "You are already following this user")
    return redirect('profile', username)

def new_chirp(request):
    if request.method == "POST":
        form = MessageForm(data=request.POST)
        if form.is_valid():
            form.save()
    return redirect("index")

@csrf_exempt
def like_message(request):
    if request.method == "POST":
        message_id = request.POST.get('id')
        print(message_id)
        like_value = bool(int(request.POST.get('like')))
        print(like_value)
        message = get_object_or_404(Message, id=message_id)
        try:
            like = Like.objects.get(user=request.user, message=message)
            if like.like == like_value:
                like.delete()
            else:
                like.like = like_value
                like.save()
        except Like.DoesNotExist:
            like = Like(user=request.user, message=message, like=like_value)
            like.save()
    return JsonResponse({'succes':'true'})