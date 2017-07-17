from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class TimestampModel(models.Model):
    class Meta:
        abstract = True
    created = models.DateTimeField(auto_now_add=True)




class Message(TimestampModel):
    user = models.ForeignKey(User)
    status = models.TextField(null=True, max_length=140, blank=False)



class Like(TimestampModel):
    user = models.ForeignKey(User)
    message = models.ForeignKey(Message)
    like = models.BooleanField(default=True)


class Follow(TimestampModel):
    followed_user = models.ForeignKey(User, related_name="followed_by")
    following_user = models.ForeignKey(User, related_name="following")

