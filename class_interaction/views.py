from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiscussionTopic, DiscussionPost, InteractionStatistics
from .forms import DiscussionTopicForm, DiscussionPostForm
from django.contrib.auth.models import User
from class_management.models import Class, Student

@login_required
def discussion_topics(request):
    topics = DiscussionTopic.objects.all()
    return render(request, 'discussion_topics.html', {'topics': topics})

@login_required
def create_topic(request):
    if request.method == 'POST':
        form = DiscussionTopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discussion_topics')
    else:
        form = DiscussionTopicForm()
    return render(request, 'create_topic.html', {'form': form})

@login_required
def topic_details(request, topic_id):
    topic = get_object_or_404(DiscussionTopic, id=topic_id)
    posts = DiscussionPost.objects.filter(topic=topic)
    return render(request, 'topic_details.html', {'topic': topic, 'posts': posts})

@login_required
def create_post(request, topic_id):
    topic = get_object_or_404(DiscussionTopic, id=topic_id)
    if request.method == 'POST':
        form = DiscussionPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_details', topic_id=topic.id)
    else:
        form = DiscussionPostForm()
    return render(request, 'create_post.html', {'form': form, 'topic': topic})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    return redirect('topic_details', topic_id=post.topic.id)

@login_required
def pin_post(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    post.is_pinned = True
    post.save()
    return redirect('topic_details', topic_id=post.topic.id)

@login_required
def interaction_statistics(request):
    stats = InteractionStatistics.objects.all()
    return render(request, 'interaction_statistics.html', {'stats': stats})

@login_required
def student_list(request, class_id):
    class_info = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(class_info=class_info)
    
    # 获取每个学生的互动统计
    student_stats = []
    for student in students:
        try:
            # 使用student_id作为用户名来查找统计信息
            stats = InteractionStatistics.objects.get(user__username=student.student_id)
            student_stats.append({
                'student': student,
                'post_count': stats.post_count,
                'reply_count': stats.reply_count,
                'total_interactions': stats.post_count + stats.reply_count
            })
        except InteractionStatistics.DoesNotExist:
            student_stats.append({
                'student': student,
                'post_count': 0,
                'reply_count': 0,
                'total_interactions': 0
            })
    
    # 按总互动次数排序
    student_stats.sort(key=lambda x: x['total_interactions'], reverse=True)
    
    return render(request, 'class_interaction/student_list.html', {
        'class_group': class_info,
        'student_stats': student_stats
    })