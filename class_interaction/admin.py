from django.contrib import admin
from .models import DiscussionTopic, DiscussionPost, InteractionStatistics


@admin.register(DiscussionTopic)
class DiscussionTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'scope', 'created_at', 'updated_at')
    list_filter = ('scope', 'created_at')
    search_fields = ('name', 'description')


@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'created_by', 'created_at', 'is_pinned')
    list_filter = ('topic', 'created_by', 'is_pinned', 'created_at')
    search_fields = ('content', 'created_by__username')


@admin.register(InteractionStatistics)
class InteractionStatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_count', 'reply_count')
    list_filter = ('user',)
    search_fields = ('user__username',)
