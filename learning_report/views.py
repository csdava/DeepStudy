from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, redirect
from django.conf import settings
from openai import OpenAI
from .models import MistakeDiagnosis, SimilarQuestion
from .forms import MistakeDiagnosisForm
import json
import os
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY', 'sk-bc14211e98e3444e96b04c818666e128'),  # 从环境变量获取
    base_url="https://api.deepseek.com"
)


def mistake_diagnosis(request):
    if request.method == 'POST':
        form = MistakeDiagnosisForm(request.POST)
        if form.is_valid():
            # 构建AI提示
            prompt = f"""请分析以下错题并给出诊断报告：

            学科：{form.cleaned_data['subject']}
            知识点：{form.cleaned_data['knowledge_point']}
            题目内容：{form.cleaned_data['question_text']}
            学生答案：{form.cleaned_data['student_answer']}
            自我分析：{form.cleaned_data['self_analysis'] or '无'}

            请按以下JSON格式返回结果：
            {{
                "analysis": {{
                    "knowledge_gaps": [],
                    "thinking_errors": [],
                    "root_cause": ""
                }},
                "recommendations": [],
                "similar_questions": []
            }}
            """

            # 调用AI接口
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位专业的教育诊断专家"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            # 解析结果
            result = json.loads(response.choices[0].message.content)

            # 保存诊断记录
            diagnosis = MistakeDiagnosis.objects.create(
                student=request.user.userprofile,
                subject=form.cleaned_data['subject'],
                knowledge_point=form.cleaned_data['knowledge_point'],
                original_question={
                    'question': form.cleaned_data['question_text'],
                    'answer': form.cleaned_data['student_answer']
                },
                diagnosis_result=result
            )

            # 获取相似题目
            similar_questions = SimilarQuestion.objects.filter(
                subject=form.cleaned_data['subject'],
                knowledge_points__contains=form.cleaned_data['knowledge_point']
            )[:5]

            return render(request, 'diagnosis_result.html', {
                'diagnosis': diagnosis,
                'similar_questions': similar_questions,
                'ai_result': result
            })
    else:
        form = MistakeDiagnosisForm()

    return render(request, 'diagnosis_form.html', {'form': form})
from django.http import HttpResponse

def report_home(request):
    return HttpResponse("欢迎来到学习报告中心")