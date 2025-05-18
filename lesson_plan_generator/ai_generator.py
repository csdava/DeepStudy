from typing import Dict, List, Optional
import logging
import os
from openai import OpenAI
from django.conf import settings

logger = logging.getLogger(__name__)

class LessonPlanAIGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY', 'sk-bc14211e98e3444e96b04c818666e128'),
            base_url="https://api.deepseek.com"
        )

    def generate_lesson_plan(self, 
                           subject: str,
                           grade: str,
                           objectives: str,
                           duration: str,
                           key_points: Optional[List[str]] = None,
                           difficulties: Optional[str] = None,
                           teaching_style: Optional[str] = None,
                           student_profile: Optional[str] = None) -> Dict:
        """
        使用AI生成教案内容
        """
        # 构建提示词
        prompt = self._build_prompt(
            subject, grade, objectives, duration,
            key_points, difficulties, teaching_style, student_profile
        )
        
        try:
            # 调用DeepSeek API生成教案内容
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的教育专家，擅长编写教案。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # 解析返回的内容
            content = response.choices[0].message.content
            return self._parse_response(content)
            
        except Exception as e:
            logger.error(f"AI生成教案失败: {str(e)}")
            raise

    def _build_prompt(self, subject, grade, objectives, duration,
                     key_points, difficulties, teaching_style, student_profile):
        """构建AI提示词"""
        prompt = f"""请为以下教学内容生成一份详细的教案，使用纯文本格式，不要使用markdown或其他标记语言：

学科：{subject}
年级：{grade}
教学目标：{objectives}
课时：{duration}

"""
        if key_points:
            prompt += f"知识点：\n" + "\n".join([f"- {point}" for point in key_points]) + "\n\n"
        
        if difficulties:
            prompt += f"教学重难点：{difficulties}\n\n"
            
        if teaching_style:
            prompt += f"教学风格：{teaching_style}\n\n"
            
        if student_profile:
            prompt += f"学生情况：{student_profile}\n\n"
            
        prompt += """请生成以下内容，使用纯文本格式，用标题和段落清晰分隔各个部分：

1. 详细的教学目标展开
请直接列出具体目标，不要使用任何特殊格式。

2. 教学步骤（包括导入、新授、练习、总结）
按照时间顺序列出每个步骤，使用自然段落描述。

3. 重难点讲解策略
用清晰的文字描述每个重难点的具体讲解方法。

4. 课堂互动设计
直接描述互动环节，包括具体的师生互动方式。

5. 课堂提问和检测题目
列出具体的问题和题目，使用自然段落。

6. PPT大纲
简单列出PPT的页面内容。

7. 课后作业建议
直接描述作业内容和要求。

注意：
- 所有内容使用纯文本格式
- 用标题和自然段落组织内容
- 不要使用特殊符号或标记
- 确保内容清晰易读
- 适合目标年级学生的认知水平
"""
        
        return prompt

    def _parse_response(self, content: str) -> Dict:
        """解析AI返回的内容"""
        # 这里可以添加更复杂的解析逻辑
        return {
            'content': content,
            'sections': {
                'objectives': self._extract_section(content, '教学目标'),
                'steps': self._extract_section(content, '教学步骤'),
                'strategies': self._extract_section(content, '重难点讲解策略'),
                'interactions': self._extract_section(content, '课堂互动设计'),
                'questions': self._extract_section(content, '课堂提问和检测题目'),
                'ppt_outline': self._extract_section(content, 'PPT大纲'),
                'homework': self._extract_section(content, '课后作业建议')
            }
        }

    def _extract_section(self, content: str, section_name: str) -> str:
        """从内容中提取特定部分"""
        try:
            # 所有可能的部分名称
            sections = [
                '教学目标', '教学步骤', '重难点讲解策略', 
                '课堂互动设计', '课堂提问和检测题目', 
                'PPT大纲', '课后作业建议'
            ]
            
            # 找到当前部分的起始位置
            start = content.find(section_name)
            if start == -1:
                return ""
                
            # 找到下一个部分的位置
            next_starts = []
            for section in sections:
                if section != section_name:
                    pos = content.find(section, start + len(section_name))
                    if pos != -1:
                        next_starts.append(pos)
            
            # 如果找到了下一个部分，使用最近的一个作为结束位置
            if next_starts:
                end = min(next_starts)
                section_content = content[start:end].strip()
            else:
                # 如果是最后一个部分，使用到末尾的所有内容
                section_content = content[start:].strip()
            
            # 移除部分标题
            if section_content.startswith(section_name):
                section_content = section_content[len(section_name):].strip()
            
            return section_content
            
        except Exception as e:
            logger.error(f"提取{section_name}部分时出错: {str(e)}")
            return "" 