from django.shortcuts import render
from django.http import JsonResponse
from .models import MistakeRecord
from .forms import MistakeDiagnosisForm

def index(request):
    """错题诊断首页"""
    return render(request, 'mistake_diagnosis/index.html')

def analyze_mistake(request):
    """分析错题"""
    if request.method == 'POST':
        form = MistakeDiagnosisForm(request.POST)
        if form.is_valid():
            # TODO: 实现错题分析逻辑
            pass
    else:
        form = MistakeDiagnosisForm()
    
    return render(request, 'mistake_diagnosis/analyze.html', {'form': form})

def history(request):
    """查看历史记录"""
    records = MistakeRecord.objects.filter(student=request.user.profile).order_by('-diagnosed_at')
    return render(request, 'mistake_diagnosis/history.html', {'records': records})
