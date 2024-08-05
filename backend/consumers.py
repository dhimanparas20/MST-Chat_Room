from channels.generic.websocket import JsonWebsocketConsumer,AsyncJsonWebsocketConsumer 
from django.contrib.auth.models import User
from .models import UserDetail, Group, GroupMessage
from .serializers import GroupSerializer,GroupMessageSerializer,UserDetailsSerializer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async ,async_to_sync
from django.shortcuts import get_object_or_404

class AsyncChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user = self.scope["user"]
        
        if (self.user != AnonymousUser()):
            group_exists = await self.get_group_data()
            
            if not group_exists:
                print(f"Crerating New group: {self.room_id}")
                data = {"owner":self.user.id,"groupKey":self.room_id,"name":f"{str(self.user)}s Room"}
                await self.create_new_group(data=data)
            
            await self.channel_layer.group_add(
                self.room_id,
                self.channel_name
            )
            await self.update_user_details(data={'online': True}) 
            await self.accept()

            self.group_data = await self.get_group_data()
            chat_history = await self.get_group_chat_history(groupKey=self.room_id)

            await (self.channel_layer.group_send(
                        self.room_id,
                        {
                            'type': 'chat_message',
                            'user': self.user.username,
                            'content': {"message":f"{self.user.username} joined the chat"}
                        }
                ))

            await (self.channel_layer.group_send(
                        self.room_id,
                        {
                            'type': 'chat_message',
                            'user': self.user.username,
                            'content': {"history":chat_history}
                        }
                ))
        
        else:    
            await self.accept()
            await self.send_json({
                "error": "Invalid User",
                "message": "Please register first",
                })
            await self.close()      

    async def disconnect(self, close_code):
        # Leave room group
        if (self.user != AnonymousUser()):
            chat_owner = str(self.group_data['owner'])
            if str(self.user.username) != chat_owner:
                await (self.channel_layer.group_send(
                        self.room_id,
                        {
                            'type': 'chat_message',
                            'user': self.user.username,
                            'content': {"message":f"user {self.user.username} left chat"}
                        }
                ))
                await self.update_user_details(data={'online': False})
                await self.channel_layer.group_discard(self.room_id,self.channel_name)
                
            else:
                # owner left the chat (Delete the group)
                await (self.channel_layer.group_send(
                        self.room_id,
                        {
                            'type': 'chat_message',
                            'user': self.user.username,
                            'content': {"message":f"owner {self.user.username} left chat. Group will be deleted"}
                        }
                ))
                await self.update_user_details(data={'online': False})
                await self.delete_group_from_db(groupKey=self.room_id)
        
        await self.close()        
        
    #Step 1 of message receiving
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if self.user != AnonymousUser():
            try:
                if text_data:
                    await self.receive_json(await self.decode_json(text_data), **kwargs)
                else:
                    raise ValueError("No text section for incoming WebSocket frame!")
            except ValueError as e:
                self.send_json({'error': str(e)})       
    
    #Step 2 of message receiving
    async def receive_json(self, content, **kwargs):
        # Send message to room group  
        group_id = self.group_data['id']
        await self.create_new_message(sender=self.user.id,group=group_id,text=content['message'])
        await (self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'content': content
            }
        ))

    # Receive message from room group
    #Step 3 of message receiving
    async def chat_message(self, event):
        try:
            content = event['content']
            await self.send_json(content)   

        except Exception as e:
            print(f"chat_message EXCEPTION: {e}")
            content = event['content']
            await self.send_json(content)      

    @database_sync_to_async
    def get_group_data(self,groupKey=None):
        if not groupKey:
            groupKey = self.room_id
        group_exists = Group.objects.filter(groupKey=groupKey).exists()
        if group_exists:
            group_owner = Group.objects.get(groupKey=groupKey).owner
            group_id = Group.objects.get(groupKey=groupKey).id
            group_name = Group.objects.get(groupKey=groupKey).name
            group_data = {"owner":group_owner,"id":group_id,"name":group_name}
            return group_data
        return False
    
    @database_sync_to_async
    def get_group_chat_history(self, groupKey):
        group = Group.objects.get(groupKey=groupKey)
        queryset = GroupMessage.objects.filter(group=group).order_by('-timestamp')
        serializer = GroupMessageSerializer(queryset, many=True)  # Serialize queryset
        serialized_data = serializer.data
        return serialized_data
    
    @database_sync_to_async
    def create_new_group(self,data):
        serializer = GroupSerializer(data=data,partial=True)
        if serializer.is_valid():
            group_instance = serializer.save()
            print(f"New group with ID '{group_instance.id}' has been created.")
            return True
        print(serializer.errors)
        return False
    
    @database_sync_to_async
    def create_new_message(self,sender,group,text):
        data = {"sender":sender,"group":group,"text":text}
        serializer = GroupMessageSerializer(data=data,partial=True)
        if serializer.is_valid():
            group_instance = serializer.save()
            return True
        print(serializer.errors)
        return False
    
    @database_sync_to_async
    def delete_group_from_db(self, groupKey):
        try:
            group_instance = Group.objects.get(groupKey=groupKey)
            group_instance.delete()
            print(f"Group with key '{groupKey}' has been deleted.")
            return True
        except Group.DoesNotExist:
            print(f"Group with key '{groupKey}' does not exist.")
            return False
     
    @database_sync_to_async
    def update_user_details(self, data):
        try:
            instance = UserDetail.objects.get(username=self.user)
            serializer = UserDetailsSerializer(instance=instance, data=data, partial=True)
            if serializer.is_valid():
                updated_instance = serializer.save()
                return True
            else:
                print(serializer.errors)
                return False
        except UserDetail.DoesNotExist:
            print(f"UserDetail for user '{self.user.username}' does not exist.")
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
