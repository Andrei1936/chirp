from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from message.views import RegisterView, TimelineView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TimelineView.as_view(), name='index'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
]