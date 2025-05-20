from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from class_management.models import Class

@login_required
def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'task_assignment/task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '任务创建成功！')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_assignment/task_form.html', {'form': form, 'title': '创建任务'})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, '任务更新成功！')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_assignment/task_form.html', {'form': form, 'title': '编辑任务'})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, '任务删除成功！')
        return redirect('task_list')
    return render(request, 'task_assignment/task_confirm_delete.html', {'task': task})
