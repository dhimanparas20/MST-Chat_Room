from django.contrib import admin
from .models import UserDetail,Group,GroupMessage
# Register your models here.

@admin.register(UserDetail)
class UserDetailsAdmin(admin.ModelAdmin):
    search_fields = ['username','email','phone_number']
    list_display = ['username','email','phone_number','online']
    list_filter = ['online']  

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ['id','groupKey','name','owner']
    list_display = ['id','groupKey','name','owner']

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    search_fields = ['id','sender','group']
    list_display = ['id','sender','group_id','text','timestamp']

# @admin.register(Conversation)
# class ConversationAdmin(admin.ModelAdmin):
#     search_fields = ['id','initiator','receiver']
#     list_display = ['id','initiator','receiver','start_time'] 

# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     search_fields = ['id','sender','conversation_id']
#     list_display = ['id','sender','conversation_id_id','text']     