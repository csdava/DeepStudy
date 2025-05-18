import requests
from datetime import datetime, timedelta


def fetch_learning_data(user):
    """示例：从学习平台API获取数据"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # 模拟API调用（需替换实际URL和认证）
    response = requests.get(
        "https://api.learning-platform.com/records",
        params={
            "user_id": user.id,
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
    return response.json() if response.status_code == 200 else None