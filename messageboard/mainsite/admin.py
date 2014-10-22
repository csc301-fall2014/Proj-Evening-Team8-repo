from django.contrib import admin
from mainsite.models import Topic, Message

# Register your models here.
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic_name']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'message_content']

admin.site.register(Topic, TopicAdmin)
admin.site.register(Message)