from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
frome infra.settings import get_settings
from infra.logging import get_logger

logger = get_logger()

DEVMATE_SYSTEM_PROMPT = """你是 DevMate, 一个严谨的研发助手，服务于一个P python / Fastapi 订单微服务团队

工作准则：
- 动手前先用write_todos 写出清晰的任务清单 并且随进展更新它。
- 写代码遵循团队规范： 类型注释齐全、函数职责单一、关键逻辑配 doc string
- 不臆测： 信息不足时先用 read_file /grep 读取相关文件再动手。
- 每次改动后 ， 用一两句话说明“改了啥为啥改”
"""

def builg_model():
    s=get_settings()
    return init_chat_model(
        model=s.syc_model_name,
        model_provider=s.syc_model_provider,
        api_key=s.syc_api_key.get_secret_value(),
        base_url=s.syc_base_url,
        max_retries=s.syc_max_retries,
        timeout=s.syc_timeout,
        temperature=0.1,
    )

def build_agent():
    model = build_model()
    agent = create_deep_agent(
        model=model,
        system_prompt=DEVMATE_SYSTEM_PROMPT,
    )
    logger.info("Agent built successfully model:{}",model.model_name)
    return agent

