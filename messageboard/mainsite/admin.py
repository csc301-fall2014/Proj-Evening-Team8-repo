from django.contrib import admin
from mainsite.models import UserProfile, Topic, Message, Group, Tag


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic_name']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_name']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'message_content']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Message)
admin.site.register(Group, GroupAdmin)
