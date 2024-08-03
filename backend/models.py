from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# User Details
class UserDetail(models.Model):
    username = models.OneToOneField(User,primary_key=True,max_length=15,on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True)
    online = models.BooleanField(default=False)
    lastseen = models.DateTimeField(auto_now_add=True)

# Group Details
class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="group_owner"
    )
    groupKey = models.CharField(max_length=10)

# Group Convo.
class GroupMessage(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="group_message_sender"
    )
    group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True, related_name="group_chat"
    )
    text = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  

# User Convo.
class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    initiator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="convo_participant"
    )
    start_time = models.DateTimeField(auto_now_add=True)

# User Message
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name='message_sender')
    text = models.CharField(max_length=200, blank=True)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE,)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)    