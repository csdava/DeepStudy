from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Task, TaskAssignment, TaskSubmission
from .forms import TaskForm, TaskAssignmentForm, TaskSubmissionForm
from django.contrib.auth.models import User

def index(request):
    return render(request, 'task_assignment/index.html')

@login_required
def task_list(request):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面')
        return redirect('task_index')
    
    tasks = Task.objects.raw('''
        SELECT id, title, description, created_at, created_by_id 
        FROM task_assignment_task 
        WHERE created_by_id = %s 
        ORDER BY created_at DESC
    ''', [request.user.id])
    return render(request, 'task_assignment/teacher/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not request.user.is_staff and not TaskAssignment.objects.filter(task=task, assigned_to=request.user).exists():
        messages.error(request, '您没有权限查看此任务')
        return redirect('task_index')
    
    if request.user.is_staff:
        assignments = TaskAssignment.objects.filter(task=task)
    else:
        assignments = TaskAssignment.objects.filter(task=task, assigned_to=request.user)
    return render(request, 'task_assignment/teacher/task_detail.html', {'task': task, 'assignments': assignments})

@login_required
def task_create(request):
    if not request.user.is_staff:
        messages.error(request, '您没有权限创建任务')
        return redirect('task_index')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, '任务创建成功！')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_assignment/teacher/task_create.html', {'form': form})

@login_required
def task_assign(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not request.user.is_staff or task.created_by != request.user:
        messages.error(request, '您没有权限分配此任务')
        return redirect('task_index')
    
    if request.method == 'POST':
        form = TaskAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.task = task
            assignment.save()
            form.save_m2m()
            messages.success(request, '任务分配成功！')
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskAssignmentForm()
    return render(request, 'task_assignment/teacher/task_assign.html', {'form': form, 'task': task})

@login_required
def task_submit(request, assignment_id):
    assignment = get_object_or_404(TaskAssignment, id=assignment_id)
    if not assignment.assigned_to.filter(id=request.user.id).exists():
        messages.error(request, '您没有权限提交此任务')
        return redirect('task_index')
    
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task_assignment = assignment
            submission.submitted_by = request.user
            submission.save()
            messages.success(request, '任务提交成功！')
            return redirect('student_task_list')
    else:
        form = TaskSubmissionForm()
    return render(request, 'task_assignment/student/task_submit.html', {'form': form, 'assignment': assignment})

@login_required
def student_task_list(request):
    if request.user.is_staff:
        messages.error(request, '教师不能访问学生任务列表')
        return redirect('task_list')
    
    assignments = TaskAssignment.objects.filter(assigned_to=request.user)
    return render(request, 'task_assignment/student/task_list.html', {'assignments': assignments})