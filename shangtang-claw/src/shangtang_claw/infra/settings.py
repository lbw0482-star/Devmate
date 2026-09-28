# 配置中枢文件，用于存储所有配置信息

from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# settings.py -> infra -> shangtang_claw -> src -> 项目根目录
_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 模型配置
    syc_model_name: str = "qwen-max"
    syc_model_provider: str = "openai"
    syc_api_key: SecretStr   #避免密钥被print/log泄露
    syc_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
  

    # 连接弹性配置
    syc_max_retries: int = 12
    syc_timeout: int = 60

    # 持久化底座配置
    syc_postgres_url: str="postgresql://syc:syc@localhost:5432/shanyang"
    syc_redis_url: str="redis://localhost:6379/0"

    # 运行配置
    syc_log_level: str = "INFO"

@lru_cache
def get_settings() -> Settings:
    return Settings()