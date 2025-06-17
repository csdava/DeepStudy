from django.shortcuts import render

def report_view(request):
    """
    渲染学习报告页面
    """
    return render(request, 'learning_report/report.html')

def report_list_view(request):
    """
    渲染学习报告列表页面
    """
    return render(request, 'learning_report/report_list.html')
