from django import forms
from .models import DiscussionTopic, DiscussionPost

class DiscussionTopicForm(forms.ModelForm):
    class Meta:
        model = DiscussionTopic
        fields = ['name', 'description', 'scope']

class DiscussionPostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ['content', 'attachment']