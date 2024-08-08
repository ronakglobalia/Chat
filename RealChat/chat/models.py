from django.db import models
from django.contrib.auth.models import User
from chat.image_validation import FileExtensionValidator
import uuid

class SingleChatGroup(models.Model):
    name = models.CharField(max_length=225, default="")
    member = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Room(models.Model):
    room_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=225, default="")
    member = models.ManyToManyField(User)

class TextMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    text_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    text_data = models.TextField()
    
    
    def __str__(self):
        return str(self.text_id)
    
Media_Type = (("IMAGE", "IMAGE"), ("PDF", "PDF"), ("DOC", "DOC"))
class MediaMessage(models.Model):
    from_user = models.OneToOneField(User, on_delete=models.CASCADE)
    to_user= models.ForeignKey(SingleChatGroup, on_delete=models.CASCADE)
    media_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    media_type = models.CharField(choices=Media_Type, max_length=20)
    media = models.FileField(upload_to="media/chat/", blank=True, null=True)
    
    def __str__(self):
        return self. media_id
    

class Message(models.Model):
    message_id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    text_message = models.ForeignKey(TextMessage, blank=True, null=True, on_delete=models.CASCADE)
    media_message = models.ForeignKey(MediaMessage, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self. message_id
