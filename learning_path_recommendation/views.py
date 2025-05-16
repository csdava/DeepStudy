from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.conf import settings
from openai import OpenAI
from .forms import StudentInfoForm
import re
import json
from pathlib import Path
import os

# ====================== 配置和初始化 ======================
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY', 'sk-bc14211e98e3444e96b04c818666e128'),  # 从环境变量获取
    base_url="https://api.deepseek.com"
)

# 资源数据库（实际应用中应该放在数据库中）
RESOURCE_DATABASE = {
    'math': {
        'video': [
            {'name': '高中数学必修一精讲', 'url': 'https://example.com/math1', 'level': 'beginner'},
            {'name': '高中数学竞赛技巧', 'url': 'https://example.com/math2', 'level': 'advanced'},
        ],
        'practice': [
            {'name': '基础题库', 'url': 'https://example.com/math_basic', 'level': 'beginner'},
            {'name': '强化练习', 'url': 'https://example.com/math_advanced', 'level': 'advanced'},
        ]
    },
    # ... 其他学科的资源
}


# ====================== 辅助解析函数 ======================
def parse_learning_path(text):
    stages = []
    current_stage = None
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 增强阶段标题匹配
        stage_match = re.match(
            r'####\s*阶段\s*([一二三四五六七八九十\d]+)\s*[：:]\s*([^（]+)(（.*）)?',
            line
        )
        if stage_match:
            if current_stage:
                stages.append(current_stage)
            current_stage = {
                'stage': stage_match.group(1).strip(),
                'title': stage_match.group(2).strip(),
                'goal': '',
                'steps': []
            }
            continue

        # 其余解析逻辑保持不变...

        # 匹配目标
        if current_stage:
            goal_match = re.match(r'^[-•*]\s*目标[：:]\s*(.+)', line)
            if goal_match:
                current_stage['goal'] = goal_match.group(1).strip()
                print(f"添加目标: {current_stage['goal']}")
                continue

            # 匹配步骤（数字编号或项目符号）
            step_match = re.match(r'^(?:\d+\.|\d+、|\d+|[-•*])\s*(.+)', line)
            if step_match and not line.startswith('目标'):
                step = step_match.group(1).strip()
                current_stage['steps'].append(step)
                print(f"添加步骤: {step}")

    # 添加最后一个阶段
    if current_stage:
        print(f"添加最后一个阶段: {current_stage}")
        stages.append(current_stage)

    print(f"解析完成，共有 {len(stages)} 个阶段")
    print("最终解析结果:", stages)
    return stages


def parse_resources(text):
    resources = []
    print("开始解析资源:", text)  # 调试输出

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue

        print(f"处理资源行: {line}")  # 调试输出

        try:
            # 匹配资源名称和类型
            resource_match = re.match(r'^[▪\-•※]?\s*([^【\[]+)(?:【(.+?)】|\[(.+?)\])?\s*(?:\((https?://\S+)\))?', line)
            if resource_match:
                name = resource_match.group(1).strip()
                type_ = resource_match.group(2) or resource_match.group(3) or '通用'
                url = resource_match.group(4)

                resource = {
                    'name': name,
                    'type': type_,
                    'url': url,
                    'level': 'beginner'  # 默认级别
                }
                resources.append(resource)
                print(f"解析到资源: {resource}")  # 调试输出

        except Exception as e:
            print(f"资源行解析失败：{line} | 错误：{str(e)}")
            continue

    print(f"资源解析结果: {resources}")  # 调试输出
    return resources


def parse_schedule(text):
    """解析时间规划内容"""
    schedule = {
        'total_time': '未指定',
        'daily_time': '未指定',
        'sequence': []
    }

    print("开始解析时间规划:", text)

    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        print(f"处理时间规划行: {line}")

        # 总耗时匹配
        total_match = re.match(r'[-•*]?\s*总耗时[：:]\s*(.+)', line)
        if total_match:
            schedule['total_time'] = total_match.group(1).strip()
            continue

        # 每日时间匹配
        daily_match = re.match(r'[-•*]?\s*每日建议[：:]\s*(.+)', line)
        if daily_match:
            schedule['daily_time'] = daily_match.group(1).strip()
            continue

        # 学习顺序匹配（只匹配实际的顺序项）
        sequence_match = re.match(r'^(?:\d+\.|\d+、|\d+)\s*(.+)', line)
        if sequence_match and not line.startswith('总耗时') and not line.startswith('每日建议'):
            schedule['sequence'].append(sequence_match.group(1).strip())

    print(f"时间规划解析结果: {schedule}")
    return schedule


def parse_ai_response(content):
    """主解析函数"""
    sections = {
        "path_map": [],
        "resources": [],
        "schedule": {
            'total_time': '未指定',
            'daily_time': '未指定',
            'sequence': []
        }
    }

    try:
        print("\n=== 开始解析AI响应 ===")
        print("原始内容:", content)

        # 使用更宽松的模式匹配各部分内容
        path_pattern = r'###\s*个性化学习路径\s*([\s\S]*?)(?=###\s*推荐学习资源|###\s*时间规划建议|\Z)'
        resources_pattern = r'###\s*推荐学习资源([\s\S]*?)(?=###|$)'
        schedule_pattern = r'###\s*时间规划建议([\s\S]*?)(?=###|$)'

        # 提取各部分内容
        path_match = re.search(path_pattern, content)
        resources_match = re.search(resources_pattern, content)
        schedule_match = re.search(schedule_pattern, content)

        print("\n--- 提取的部分 ---")
        if path_match:
            path_content = path_match.group(1).strip()
            print("学习路径内容:", path_content)
            sections["path_map"] = parse_learning_path(path_content)
        else:
            print("未找到学习路径部分")

        if resources_match:
            resources_content = resources_match.group(1).strip()
            print("资源内容:", resources_content)
            sections["resources"] = parse_resources(resources_content)
        else:
            print("未找到资源部分")

        if schedule_match:
            schedule_content = schedule_match.group(1).strip()
            print("时间规划内容:", schedule_content)
            sections["schedule"] = parse_schedule(schedule_content)
        else:
            print("未找到时间规划部分")

        print("\n--- 解析结果 ---")
        print("学习路径:", sections["path_map"])
        print("资源:", sections["resources"])
        print("时间规划:", sections["schedule"])

    except Exception as e:
        print(f"解析错误：{str(e)}")
        import traceback
        print(traceback.format_exc())

    return sections


# 在调用parse_ai_response后添加

# ====================== 辅助函数 ======================
def generate_mermaid_diagram(stages):
    """生成Mermaid.js格式的学习路径图"""
    if not stages:
        return "graph TD; A[暂无学习路径数据]"

    print("生成图表的输入数据:", stages)  # 调试输出

    mermaid_code = ["graph TD;"]

    # 添加样式定义
    mermaid_code.append("classDef stage fill:#e1f5fe,stroke:#01579b,stroke-width:2px;")
    mermaid_code.append("classDef step fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;")

    for i, stage in enumerate(stages, 1):
        stage_id = f"S{i}"
        stage_title = f"{stage.get('stage', str(i))}. {stage.get('title', '未命名阶段')}"
        mermaid_code.append(f'{stage_id}["{stage_title}"]')
        mermaid_code.append(f'class {stage_id} stage;')

        # 添加目标节点
        goal_id = f"G{i}"
        goal_text = stage.get('goal', '暂无目标').replace('"', "'")
        mermaid_code.append(f'{goal_id}["目标: {goal_text}"]')
        mermaid_code.append(f'{stage_id} --> {goal_id}')

        # 添加步骤节点
        steps = stage.get('steps', [])
        for j, step in enumerate(steps, 1):
            step_id = f"S{i}_Step{j}"
            step_text = step.replace('"', "'")
            mermaid_code.append(f'{step_id}["{j}. {step_text}"]')
            mermaid_code.append(f'{goal_id} --> {step_id}')
            mermaid_code.append(f'class {step_id} step;')

        # 连接各阶段
        if i > 1:
            mermaid_code.append(f'S{i - 1} --> S{i}')

    print("生成的Mermaid代码:", "\\n".join(mermaid_code))  # 调试输出
    return "\\n".join(mermaid_code)


def match_resources(subject, progress_level, learning_style):
    """根据学生特征匹配合适的学习资源"""
    matched_resources = []

    if subject in RESOURCE_DATABASE:
        subject_resources = RESOURCE_DATABASE[subject]

        # 根据学习风格选择资源类型
        preferred_types = {
            'visual': ['video', 'animation'],
            'auditory': ['audio', 'video'],
            'reading': ['text', 'ebook'],
            'kinesthetic': ['practice', 'interactive']
        }

        preferred = preferred_types.get(learning_style, [])

        # 根据进度级别筛选资源
        progress_mapping = {
            'beginner': ['beginner'],
            'intermediate': ['beginner', 'intermediate'],
            'advanced': ['intermediate', 'advanced'],
            'expert': ['advanced', 'expert']
        }

        suitable_levels = progress_mapping.get(progress_level, ['beginner'])

        # 遍历所有资源类型
        for resource_type, resources in subject_resources.items():
            if resource_type in preferred:
                for resource in resources:
                    if resource['level'] in suitable_levels:
                        matched_resources.append(resource)

    return matched_resources


def analyze_learning_status(form_data):
    """分析学生学习状态"""
    status = {
        'level': form_data['current_progress'],
        'strengths': [],
        'weaknesses': [],
        'recommendations': []
    }

    # 分析考试成绩
    if form_data.get('recent_scores'):
        scores = [int(s.strip()) for s in form_data['recent_scores'].split(',') if s.strip().isdigit()]
        if scores:
            avg_score = sum(scores) / len(scores)
            trend = 'improving' if scores[-1] > scores[0] else 'declining'
            status['score_trend'] = trend
            status['average_score'] = avg_score

    # 根据进度和目标给出建议
    if form_data['current_progress'] == 'beginner':
        status['recommendations'].append('建议从基础知识开始，打好基础')
    elif form_data['current_progress'] == 'advanced':
        status['recommendations'].append('可以开始尝试更具挑战性的题目')

    return status


# ====================== 视图函数 ======================
def learning_path_recommendation(request):
    context = {
        'form': StudentInfoForm(),
        'error_message': None,
        'path_map': [],
        'resources': [],
        'schedule': {},
        'visualization': '',
        'learning_status': {},
        'raw_content': ''
    }

    if request.method == 'POST':
        form = StudentInfoForm(request.POST)
        if not form.is_valid():
            context['error_message'] = '表单验证失败'
            return render(request, 'learning_path_form.html', context)

        try:
            data = form.cleaned_data

            # 分析学习状态
            learning_status = analyze_learning_status(data)

            # 构建更结构化的AI提示
            prompt = f"""
请严格按照以下格式生成学习规划方案。注意：必须保持格式标记的准确性，这对后续处理至关重要。

### 个性化学习路径
#### 阶段1：基础巩固
- 目标：[具体目标描述]
1. [具体步骤1]
2. [具体步骤2]
3. [具体步骤3]

#### 阶段2：[阶段名称]
- 目标：[具体目标描述]
1. [具体步骤1]
2. [具体步骤2]
3. [具体步骤3]
### 推荐学习资源
- [资源名称1]【视频】(https://example.com/resource1)
- [资源名称2]【练习】(https://example.com/resource2)
- [资源名称3]【文档】(https://example.com/resource3)

### 时间规划建议
- 总耗时：[具体时间，如：4周]
- 每日建议：[具体时间，如：2小时]
- 学习顺序：
1. [具体安排1]
2. [具体安排2]
3. [具体安排3]

请基于以下学生信息，按上述格式生成完整的学习规划：

1. 基本信息：
- 学科：{data['subject']}
- 当前水平：{data['current_progress']}（{data.get('progress_detail', '')}）
- 学习目标：{', '.join(data['learning_goal'])}（{data.get('goal_detail', '')}）
- 学习风格：{data['learning_style']}
- 可用时间：每天{data['learning_time']}分钟

2. 学习状态：
- 进度：{learning_status.get('level')}
- 成绩趋势：{learning_status.get('score_trend', 'N/A')}

请确保：
1. 严格遵循上述格式标记
2. 每个阶段都包含目标和具体步骤
3. 资源推荐要带有类型标记【】和链接()
4. 时间规划要包含总耗时、每日建议和具体顺序
"""

            # 调用API获取响应
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位专业的教育规划专家。
请严格按照用户提供的格式生成内容。
格式的准确性对后续处理非常重要。
使用markdown标题层级（###和####）来标记不同部分。
确保每个部分的格式标记完全匹配要求。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2048,  # 增加token限制
                temperature=0.7
            )

            if not response.choices:
                raise ValueError("未收到有效响应")

            # 获取并解析原始内容
            raw_content = response.choices[0].message.content
            print("AI返回的原始内容：", raw_content)  # 调试输出

            structured_data = parse_ai_response(raw_content)
            print("解析后的结构化数据：", structured_data)  # 调试输出

            # 生成可视化图表
            if structured_data['path_map']:
                mermaid_diagram = generate_mermaid_diagram(structured_data['path_map'])
            else:
                mermaid_diagram = "graph TD; A[无数据]"
            print("生成的图表代码：", mermaid_diagram)  # 调试输出

            # 匹配学习资源
            matched_resources = match_resources(
                data['subject'],
                data['current_progress'],
                data['learning_style']
            )
            print("匹配的资源：", matched_resources)  # 调试输出

            # 更新上下文
            context.update({
                'path_map': structured_data.get('path_map', []),
                'resources': matched_resources or structured_data.get('resources', []),  # 优先使用匹配的资源
                'schedule': structured_data.get('schedule', {}),
                'visualization': mermaid_diagram,
                'learning_status': learning_status,
                'raw_content': mark_safe(raw_content.replace('\n', '<br>'))
            })

            return render(request, 'learning_path_result.html', context)

        except Exception as e:
            import traceback
            print("错误详情：", traceback.format_exc())  # 详细错误信息
            context['error_message'] = f'服务暂不可用：{str(e)}'
            return render(request, 'error.html', context)

    return render(request, 'learning_path_form.html', context)


def redirect_to_form(request):
    return redirect('learning_path')
