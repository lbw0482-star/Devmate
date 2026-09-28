# 启动期间自检
import asyncio
import sys

import psycopg
import redis.asyncio as aioredis
from shangtang_claw.infra.settings import get_settings


async def main():
    s=get_settings()
    print("环境配置自检通过：")
    print(f"模型：{s.syc_model_name}")
    print(f"API密钥：{s.syc_api_key.get_secret_value()}")
    print(f"持久化底座：{s.syc_postgres_url}")
    print(f"Redis URL：{s.syc_redis_url}")
    print(f"日志级别：{s.syc_log_level}")
    print("所有配置自检通过！")

    # Postgresql 异步链接
    aconn =await psycopg.AsyncConnection.connect(s.syc_postgres_url)
    async with aconn:
        cur=await aconn.execute("SELECT 1")
        ver= (await cur.fetchone())[0]
        print(f"Postgresql 连接成功，版本：{ver}")

    # Redis 异步链接
    rconn = await aioredis.from_url(s.syc_redis_url)
    pong =await rconn.ping()
    await rconn.aclose()
    print(f"Redis 连接成功，版本：{pong}")

if __name__ == "__main__":
     # 在Windows上使用SelectorEventLoop
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    print("所有自检通过！")