from django.contrib import admin
from mainsite.models import UserProfile, Topic, Message

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic_name']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'message_content']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Message)