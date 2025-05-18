import os
from openai import OpenAI


def generate_ai_advice(**data):
    # 初始化 DeepSeek 客户端
    client = OpenAI(
        api_key=os.getenv('DEEPSEEK_API_KEY', 'sk-bc14211e98e3444e96b04c818666e128'),
        base_url="https://api.deepseek.com"
    )

    prompt = f"""
    根据以下学习数据生成周报建议：
    - 总学习时长: {data['learning_data']['total_duration']} 分钟
    - 作业正确率: {data['assignment_data']['accuracy']}%
    - 主要薄弱知识点: {', '.join(data['test_data']['weak_points'])}

    请用简洁的中文给出学习建议，包含：
    1. 本周学习情况总结
    2. 需要加强的知识点
    3. 推荐的学习资源
    4. 下周学习计划建议
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"建议生成失败：{str(e)}"