# 在文件底部新增
ENV_FILE_PATH = BASE_DIR / '.env'
if ENV_FILE_PATH.exists():
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE_PATH)

DEEPSEEK_CONFIG = {
    'api_version': 'v1',
    'timeout': 20.0,
    'max_retries': 3
}