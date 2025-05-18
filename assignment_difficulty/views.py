from django.shortcuts import render, redirect
from django.conf import settings
from openai import OpenAI
from .models import DifficultyAnalysis
from .forms import DifficultyOptimizationForm
import json
import uuid
import os

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY', 'sk-bc14211e98e3444e96b04c818666e128'),  # 从环境变量获取
    base_url="https://api.deepseek.com"
)


def analyze_difficulty(request):
    if request.method == 'POST':
        form = DifficultyOptimizationForm(request.POST)
        if form.is_valid():
            try:
                # 构建AI提示
                prompt = f"""
                请作为教育专家，根据以下信息进行作业难度分析和优化建议：

                基本信息：
                - 学科：{form.cleaned_data['subject']}
                - 年级：{form.cleaned_data['grade']}
                - 作业目标：{form.cleaned_data['learning_objectives']}

                作业内容：
                {form.cleaned_data['assignment_content']}

                学生学情数据：
                - 班级平均分：{form.cleaned_data['student_performance'].get('average_score', '未提供')}
                - 成绩分布：{form.cleaned_data['student_performance'].get('score_distribution', '未提供')}
                - 常见错误：{form.cleaned_data['student_performance'].get('common_mistakes', '未提供')}
                - 补充说明：{form.cleaned_data['student_performance'].get('additional_notes', '未提供')}

                请提供详细的分析报告，包含以下内容（必须使用JSON格式）：

                {{
                    "difficulty_level": "过于简单/偏简单/适中/偏难/过于困难",
                    "knowledge_coverage": {{
                        "covered_points": ["知识点1", "知识点2", ...],
                        "difficulty_analysis": {{
                            "知识点1": {{
                                "difficulty": "简单/中等/困难",
                                "reason": "难度判断原因"
                            }},
                            ...
                        }}
                    }},
                    "thinking_levels": {{
                        "remember": 百分比,
                        "understand": 百分比,
                        "apply": 百分比,
                        "analyze": 百分比,
                        "evaluate": 百分比,
                        "create": 百分比
                    }},
                    "difficulty_adjustment": [
                        {{
                            "suggestion": "具体建议",
                            "reason": "建议原因",
                            "example": "示例题目或修改方案"
                        }},
                        ...
                    ],
                    "question_type_suggestions": [
                        {{
                            "type": "题型",
                            "reason": "建议原因",
                            "example": "示例题目"
                        }},
                        ...
                    ],
                    "sequence_optimization": {{
                        "current_sequence": ["当前题目顺序"],
                        "suggested_sequence": ["建议题目顺序"],
                        "explanation": "调整原因"
                    }},
                    "personalized_suggestions": {{
                        "advanced_students": ["针对优秀学生的建议"],
                        "intermediate_students": ["针对中等生的建议"],
                        "struggling_students": ["针对学困生的建议"]
                    }},
                    "visualization_data": {{
                        "difficulty_distribution": {{
                            "labels": ["简单", "中等", "困难"],
                            "data": [30, 40, 30]
                        }},
                        "thinking_level_distribution": {{
                            "labels": ["记忆", "理解", "应用", "分析", "评价", "创造"],
                            "data": [20, 30, 25, 15, 5, 5]
                        }},
                        "student_performance_match": {{
                            "labels": ["题目难度过低", "难度适中", "题目难度过高"],
                            "data": [20, 60, 20]
                        }}
                    }}
                }}
                """

                # 调用AI接口
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是专业的教育分析专家，擅长作业难度分析和优化建议。请确保所有输出严格遵循JSON格式。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )

                # 解析结果
                raw_content = response.choices[0].message.content
                cleaned_content = raw_content.strip().replace('```json', '').replace('```', '')
                analysis_result = json.loads(cleaned_content)

                # 创建分析记录
                analysis = DifficultyAnalysis.objects.create(
                    assignment_id=uuid.uuid4(),
                    subject=form.cleaned_data['subject'],
                    grade=form.cleaned_data['grade'],
                    assignment_content=form.cleaned_data['assignment_content'],
                    learning_objectives=form.cleaned_data['learning_objectives'],
                    student_performance=form.cleaned_data['student_performance'],
                    difficulty_level=analysis_result['difficulty_level'],
                    knowledge_coverage=analysis_result['knowledge_coverage'],
                    thinking_levels=analysis_result['thinking_levels'],
                    difficulty_adjustment=analysis_result['difficulty_adjustment'],
                    question_type_suggestions=analysis_result['question_type_suggestions'],
                    sequence_optimization=analysis_result['sequence_optimization'],
                    personalized_suggestions=analysis_result['personalized_suggestions'],
                    visualization_data=analysis_result['visualization_data']
                )

                return redirect('analysis_result', analysis_id=analysis.id)

            except Exception as e:
                return render(request, 'assignment_difficulty/error.html', {
                    'error_message': f'分析失败：{str(e)}',
                    'raw_response': raw_content if 'raw_content' in locals() else ''
                })
    else:
        form = DifficultyOptimizationForm()

    return render(request, 'assignment_difficulty/analysis_form.html', {'form': form})

def analysis_result(request, analysis_id):
    try:
        analysis = DifficultyAnalysis.objects.get(id=analysis_id)
        context = {
            'analysis': analysis,
            'difficulty_level': analysis.get_difficulty_level_display(),
            'knowledge_coverage': analysis.knowledge_coverage,
            'thinking_levels': analysis.thinking_levels,
            'difficulty_adjustment': analysis.difficulty_adjustment,
            'question_type_suggestions': analysis.question_type_suggestions,
            'sequence_optimization': analysis.sequence_optimization,
            'personalized_suggestions': analysis.personalized_suggestions,
            'visualization_data': analysis.visualization_data
        }
        return render(request, 'assignment_difficulty/analysis_result.html', context)
    except DifficultyAnalysis.DoesNotExist:
        return render(request, 'assignment_difficulty/error.html', {
            'error_message': '分析记录不存在'
        })