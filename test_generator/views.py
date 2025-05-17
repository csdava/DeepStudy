from django.shortcuts import render, redirect
from django.conf import settings
from openai import OpenAI
from .models import GeneratedTest
from .forms import TestGenerationForm
import json
import uuid
import os

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY', 'sk-bc14211e98e3444e96b04c818666e128'),
    base_url="https://api.deepseek.com"
)

def generate_test(request):
    if request.method == 'POST':
        form = TestGenerationForm(request.POST)
        if form.is_valid():
            try:
                # 构建AI提示
                prompt = f"""
                请根据以下要求生成测试题（严格使用JSON格式）：
                - 知识点：{form.cleaned_data['knowledge_point']}
                - 题型：{form.cleaned_data['question_type']}
                - 数量：{form.cleaned_data['quantity']}
                - 难度：{form.cleaned_data['difficulty']}

                输出格式要求：
                {{
                    "questions": [
                        {{
                            "question": "题目文本",
                            "options": ["选项1", "选项2", ...],  # 选择题需要
                            "answer": "正确答案",
                            "analysis": "解题思路"
                        }}
                    ]
                }}
                """

                # 调用API
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是专业试题生成专家，严格按照用户要求生成测试题"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )

                # 解析响应
                raw_content = response.choices[0].message.content
                cleaned_content = raw_content.strip().replace('```json', '').replace('```', '')
                questions = json.loads(cleaned_content)['questions']

                # 生成唯一测试链接
                test_uuid = uuid.uuid4().hex[:8]
                test_link = f"/test/{test_uuid}/"

                # 保存到session而不是数据库
                request.session[f'test_{test_uuid}'] = {
                    'knowledge_point': form.cleaned_data['knowledge_point'],
                    'question_type': form.cleaned_data['question_type'],
                    'quantity': form.cleaned_data['quantity'],
                    'difficulty': form.cleaned_data['difficulty'],
                    'generated_content': questions,
                }

                return redirect('test_preview', uuid=test_uuid)

            except Exception as e:
                return render(request, 'test_generator/error.html', {
                    'error_message': f'生成失败：{str(e)}',
                    'raw_response': raw_content if 'raw_content' in locals() else ''
                })
    else:
        form = TestGenerationForm()

    return render(request, 'test_generator/generate_test.html', {'form': form})

def test_preview(request, uuid):
    try:
        # 从session获取测试数据
        test_data = request.session.get(f'test_{uuid}')
        if not test_data:
            return render(request, 'test_generator/error.html', {'error_message': '测试不存在或已过期'})
            
        return render(request, 'test_generator/test_preview.html', {
            'test': test_data,
            'questions': test_data['generated_content']
        })
    except Exception as e:
        return render(request, 'test_generator/error.html', {'error_message': f'预览失败：{str(e)}'})

def index(request):
    """Test Generator home page view"""
    return render(request, 'test_generator/index.html')