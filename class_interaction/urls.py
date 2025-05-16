from django.urls import path
from . import views

app_name = 'class_interaction'

urlpatterns = [
    path('', views.discussion_topics, name='discussion_topics'),
    path('create_topic/', views.create_topic, name='create_topic'),
    path('topic/<int:topic_id>/', views.topic_details, name='topic_details'),
    path('topic/<int:topic_id>/create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/pin/', views.pin_post, name='pin_post'),
    path('statistics/', views.interaction_statistics, name='interaction_statistics'),
    path('student_list/<int:class_id>/', views.student_list, name='student_list'),
]