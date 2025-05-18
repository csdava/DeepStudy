from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Sum, Count
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import logging
from .models import (
    LearningRecord, AssignmentRecord, TestRecord,
    InteractionRecord, WeeklyReport
)
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from openai import OpenAI
import json
import os
from datetime import datetime, timedelta
import traceback
from django.db import models

# 配置日志
logger = logging.getLogger(__name__)

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY', 'sk-bc14211e98e3444e96b04c818666e128'),
    base_url="https://api.deepseek.com"
)

def generate_charts(report_data):
    """生成可视化图表"""
    charts = {}
    
    # 1. 学习时间分布饼图
    if report_data['resource_usage_stats']:
        fig = px.pie(
            values=list(report_data['resource_usage_stats'].values()),
            names=list(report_data['resource_usage_stats'].keys()),
            title='学习时间分布'
        )
        charts['time_distribution'] = fig.to_html(full_html=False)

    # 2. 各科目成绩雷达图
    if report_data['subject_performance']:
        subjects = list(report_data['subject_performance'].keys())
        scores = [data['score'] for data in report_data['subject_performance'].values()]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=subjects,
            fill='toself'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title='各科目表现'
        )
        charts['subject_performance'] = fig.to_html(full_html=False)

    # 3. 知识点掌握程度热力图
    if report_data['knowledge_mastery']:
        knowledge_data = []
        for subject, points in report_data['knowledge_mastery'].items():
            for point, mastery in points.items():
                knowledge_data.append({
                    'subject': subject,
                    'point': point,
                    'mastery': mastery
                })
        
        if knowledge_data:
            df = pd.DataFrame(knowledge_data)
            fig = px.density_heatmap(
                df,
                x='subject',
                y='point',
                z='mastery',
                title='知识点掌握程度'
            )
            charts['knowledge_mastery'] = fig.to_html(full_html=False)

    # 4. 作业完成情况柱状图
    fig = go.Figure(data=[
        go.Bar(name='提交率', x=['作业完成情况'], y=[report_data['avg_submission_rate']]),
        go.Bar(name='正确率', x=['作业完成情况'], y=[report_data['avg_accuracy_rate']])
    ])
    fig.update_layout(barmode='group', title='作业完成情况')
    charts['assignment_stats'] = fig.to_html(full_html=False)

    return charts

def generate_ai_analysis(report_data):
    """使用AI生成分析报告"""
    prompt = f"""
请根据以下学习数据生成一份详细的周学习分析报告。报告应包含三个部分：表现分析、改进建议和下周计划。

学习数据：
1. 总学习时长：{report_data['total_study_time']}分钟
2. 平均作业提交率：{report_data['avg_submission_rate']}%
3. 平均作业正确率：{report_data['avg_accuracy_rate']}%
4. 平均测试分数：{report_data['avg_test_score']}分
5. 互动次数：{report_data['interaction_count']}次
6. 各科目表现：{json.dumps(report_data['subject_performance'], ensure_ascii=False)}
7. 知识点掌握情况：{json.dumps(report_data['knowledge_mastery'], ensure_ascii=False)}

请按以下格式生成报告：

### 本周表现分析
[分析本周的学习情况，包括时间投入、作业完成、测试成绩等方面的表现]

### 改进建议
[针对性地提出具体的改进建议，重点关注表现欠佳的方面]

### 下周学习计划
[制定具体的下周学习计划，包括时间分配、重点科目、需要加强的知识点等]
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一位专业的教育顾问，请根据学生的学习数据生成详细的分析报告。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )

        if response.choices:
            content = response.choices[0].message.content
            # 解析AI返回的内容
            sections = content.split('###')
            analysis = ''
            suggestions = ''
            plan = ''
            
            for section in sections:
                if '本周表现分析' in section:
                    analysis = section.replace('本周表现分析', '').strip()
                elif '改进建议' in section:
                    suggestions = section.replace('改进建议', '').strip()
                elif '下周学习计划' in section:
                    plan = section.replace('下周学习计划', '').strip()
            
            return {
                'performance_analysis': analysis,
                'improvement_suggestions': suggestions,
                'next_week_plan': plan
            }
    except Exception as e:
        print(f"AI分析生成错误：{str(e)}")
        return {
            'performance_analysis': '暂时无法生成分析。',
            'improvement_suggestions': '暂时无法生成建议。',
            'next_week_plan': '暂时无法生成计划。'
        }

def generate_weekly_report(request):
    """生成周报"""
    try:
        # 获取本周的起止时间
        today = datetime.now()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        week = f"{today.year}W{today.isocalendar()[1]}"  # 格式：YYYYWW
        
        # 1. 基础学习记录
        learning_records = LearningRecord.objects.filter(
            date__range=[start_date, end_date]
        )
        
        # 2. 作业记录
        assignment_records = AssignmentRecord.objects.filter(
            week=week
        )
        
        # 3. 测试记录
        test_records = TestRecord.objects.filter(
            week=week
        )
        
        # 4. 互动记录
        interaction_records = InteractionRecord.objects.filter(
            date__range=[start_date, end_date]
        )
        
        # 5. 从其他应用收集数据
        # 5.1 错题记录
        from mistake_diagnosis.models import MistakeRecord
        mistake_records = MistakeRecord.objects.filter(
            diagnosed_at__range=[start_date, end_date]
        )
        
        # 5.2 资源使用情况
        from resource_library.models import Resource
        resource_usage = Resource.objects.filter(
            created_at__range=[start_date, end_date]
        ).values('resource_type').annotate(count=models.Count('id'))
        
        # 5.3 作业提交记录
        from task_assignment.models import Submission
        submissions = Submission.objects.filter(
            submitted_at__range=[start_date, end_date]
        )
        
        # 5.4 学习路径推荐
        from learning_path_recommendation.models import LearningPath
        learning_paths = LearningPath.objects.filter(
            generated_at__range=[start_date, end_date]
        )
        
        # 计算统计数据
        total_study_time = sum(record.study_duration for record in learning_records)
        avg_submission_rate = (
            sum(record.submission_rate for record in assignment_records) / 
            len(assignment_records) if assignment_records else 0
        )
        avg_accuracy_rate = (
            sum(record.accuracy_rate for record in assignment_records) / 
            len(assignment_records) if assignment_records else 0
        )
        avg_test_score = (
            sum(record.score for record in test_records) / 
            len(test_records) if test_records else 0
        )
        interaction_count = len(interaction_records)
        
        # 整理科目表现数据和知识点掌握情况
        subject_performance = {}
        knowledge_mastery = {}
        for test in test_records:
            if test.subject not in subject_performance:
                subject_performance[test.subject] = {
                    'score': test.score,
                    'wrong_questions': test.wrong_questions,
                    'knowledge_points': test.knowledge_points,
                    'mistake_count': len([m for m in mistake_records if m.analysis_result.get('subject') == test.subject]),
                    'submission_count': len([s for s in submissions if s.assignment.target_class.subject == test.subject])
                }
                # 从测试记录中提取知识点掌握情况
                knowledge_mastery[test.subject] = test.knowledge_points
        
        # 整理资源使用统计
        resource_usage_stats = {
            item['resource_type']: item['count'] 
            for item in resource_usage
        }
        
        # 生成AI分析
        ai_analysis = generate_ai_analysis({
            'total_study_time': total_study_time,
            'avg_submission_rate': avg_submission_rate,
            'avg_accuracy_rate': avg_accuracy_rate,
            'avg_test_score': avg_test_score,
            'interaction_count': interaction_count,
            'subject_performance': subject_performance,
            'knowledge_mastery': knowledge_mastery,
            'resource_usage': resource_usage_stats,
            'mistake_analysis': {
                'total_mistakes': len(mistake_records),
                'by_subject': {subject: len([m for m in mistake_records if m.analysis_result.get('subject') == subject])
                             for subject in set(test.subject for test in test_records)}
            },
            'learning_path_updates': [
                {
                    'path': path.recommended_path,
                    'effectiveness': path.effectiveness
                }
                for path in learning_paths
            ]
        })
        
        # 生成图表数据
        charts_data = generate_charts({
            'total_study_time': total_study_time,
            'avg_submission_rate': avg_submission_rate,
            'avg_accuracy_rate': avg_accuracy_rate,
            'avg_test_score': avg_test_score,
            'interaction_count': interaction_count,
            'subject_performance': subject_performance,
            'resource_usage_stats': resource_usage_stats,
            'knowledge_mastery': knowledge_mastery,
            'mistake_distribution': {
                subject: len([m for m in mistake_records if m.analysis_result.get('subject') == subject])
                for subject in set(test.subject for test in test_records)
            }
        })
        
        # 尝试获取已存在的周报，如果不存在则创建新的
        report, created = WeeklyReport.objects.update_or_create(
            week=week,
            defaults={
                'start_date': start_date,
                'end_date': end_date,
                'total_study_time': total_study_time,
                'avg_submission_rate': avg_submission_rate,
                'avg_accuracy_rate': avg_accuracy_rate,
                'avg_test_score': avg_test_score,
                'interaction_count': interaction_count,
                'subject_performance': subject_performance,
                'knowledge_mastery': knowledge_mastery,
                'resource_usage_stats': resource_usage_stats,
                'performance_analysis': ai_analysis.get('performance_analysis', ''),
                'improvement_suggestions': ai_analysis.get('improvement_suggestions', ''),
                'next_week_plan': ai_analysis.get('next_week_plan', ''),
                'visualization_data': {'charts': charts_data}
            }
        )
        
        logger.info(f"{'Created' if created else 'Updated'} weekly report {report.id}")
        return render(request, 'learning_report/report_detail.html', {'report': report})
        
    except Exception as e:
        logger.error(f"Error in generate_weekly_report: {str(e)}")
        return render(request, 'learning_report/error.html', {
            'error_message': f'生成周报时出错，请稍后重试。错误详情：{str(e)}'
        })

def generate_study_time_chart(records):
    """生成学习时间分布图表"""
    try:
        dates = [record.date for record in records]
        durations = [record.study_duration for record in records]
        
        fig = go.Figure(data=[
            go.Bar(x=dates, y=durations, name='学习时长')
        ])
        
        fig.update_layout(
            title='每日学习时长分布',
            xaxis_title='日期',
            yaxis_title='时长（分钟）',
            showlegend=True
        )
        
        return fig.to_dict()
    except Exception as e:
        logger.error(f"Error in generate_study_time_chart: {str(e)}")
        return None

def generate_assignment_chart(records):
    """生成作业完成情况图表"""
    try:
        weeks = [record.week for record in records]
        rates = [record.submission_rate for record in records]
        
        fig = go.Figure(data=[
            go.Scatter(x=weeks, y=rates, name='提交率', mode='lines+markers')
        ])
        
        fig.update_layout(
            title='作业提交率趋势',
            xaxis_title='周',
            yaxis_title='提交率（%）',
            showlegend=True
        )
        
        return fig.to_dict()
    except Exception as e:
        logger.error(f"Error in generate_assignment_chart: {str(e)}")
        return None

def generate_test_chart(records):
    """生成测试成绩图表"""
    try:
        weeks = [record.week for record in records]
        scores = [record.score for record in records]
        
        fig = go.Figure(data=[
            go.Scatter(x=weeks, y=scores, name='分数', mode='lines+markers')
        ])
        
        fig.update_layout(
            title='测试成绩趋势',
            xaxis_title='周',
            yaxis_title='分数',
            showlegend=True
        )
        
        return fig.to_dict()
    except Exception as e:
        logger.error(f"Error in generate_test_chart: {str(e)}")
        return None

def generate_interaction_chart(records):
    """生成互动参与度图表"""
    try:
        dates = [record.date for record in records]
        counts = [1] * len(records)  # 每个记录算一次互动
        
        fig = go.Figure(data=[
            go.Bar(x=dates, y=counts, name='互动次数')
        ])
        
        fig.update_layout(
            title='每日互动次数',
            xaxis_title='日期',
            yaxis_title='次数',
            showlegend=True
        )
        
        return fig.to_dict()
    except Exception as e:
        logger.error(f"Error in generate_interaction_chart: {str(e)}")
        return None

def view_report_list(request):
    print("=== view_report_list called ===")
    try:
        reports = WeeklyReport.objects.all().order_by('-created_at')
        print("=== WeeklyReport count:", reports.count())
        return render(request, 'learning_report/report_list.html', {'reports': reports})
    except Exception as e:
        print("=== view_report_list except ===")
        print(traceback.format_exc())
        return render(request, 'learning_report/error.html', {
            'error_message': f'获取报告列表时出错，请稍后重试。错误详情：{e}'
        })

def view_report_detail(request, report_id):
    """查看报告详情"""
    try:
        report = get_object_or_404(WeeklyReport, id=report_id)
        logger.info(f"Viewing report {report_id}")
        return render(request, 'learning_report/report_detail.html', {'report': report})
    except Http404:
        logger.warning(f"Report {report_id} not found")
        return render(request, 'learning_report/error.html', {
            'error_message': '未找到指定的报告。'
        })
    except Exception as e:
        logger.error(f"Error in view_report_detail: {str(e)}")
        return render(request, 'learning_report/error.html', {
            'error_message': '加载报告详情时出错，请稍后重试。'
        })