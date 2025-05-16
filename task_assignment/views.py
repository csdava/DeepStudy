from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Task, Assignment, Submission
from .forms import TaskForm, AssignmentForm, SubmissionForm

def index(request):
    return render(request, 'index.html')

# Teacher Views
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_assignment:assign_task', task_id=task.id)
    else:
        form = TaskForm()
    return render(request, 'teacher/create_task.html', {'form': form})

@login_required
def assign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.task = task
            assignment.save()
            return redirect('task_assignment:view_submissions', task_id=task.id)
    else:
        form = AssignmentForm()
    return render(request, 'teacher/assign_task.html', {'form': form, 'task': task})

@login_required
def grade_task(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    if request.method == 'POST':
        grade = request.POST.get('grade')
        submission.grade = float(grade)
        submission.save()
        return redirect('task_assignment:view_submissions', task_id=submission.assignment.task.id)
    return render(request, 'teacher/grade_task.html', {'submission': submission})

@login_required
def view_submissions(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    submissions = task.assignments.all()
    return render(request, 'teacher/view_submissions.html', {'task': task, 'submissions': submissions})

# Student Views
@login_required
def view_tasks(request):
    assignments = request.user.assigned_tasks.all()
    return render(request, 'student/view_tasks.html', {'assignments': assignments})

@login_required
def submit_task(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.submitted_by = request.user
            submission.save()
            return redirect('task_assignment:view_tasks')
    else:
        form = SubmissionForm()
    return render(request, 'student/submit_task.html', {'form': form, 'assignment': assignment})

@login_required
def view_grades(request):
    submissions = request.user.submissions.all()
    return render(request, 'student/view_grades.html', {'submissions': submissions})