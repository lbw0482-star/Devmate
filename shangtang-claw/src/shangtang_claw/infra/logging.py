# 日志配置 基于loguru
import sys
from pathlib import Path

from loguru import logger
from shangtang_claw.infra.settings import get_settings

_CONFIGURED = False

def setup_logging() -> None:
    # 初始化全局日志
    global _CONFIGURED
    if _CONFIGURED:
        return
    level=get_settings().syc_log_level

    logger.remove() # 移除所有默认的处理器

    #控制台输出 ： 彩色带模块位置
    logger.add(
        sys.stdout,
        level=level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        backtrace=True,
        diagnose=True, # 输出诊断信息 生产环境需要改为false
        colorize=True,
    )


    # 文件输出：按天分割
    # logging.py -> infra -> shangtang_claw -> src -> 项目根目录
    log_dir = Path(__file__).resolve().parents[3] / "logs"
    log_dir.mkdir( exist_ok=True)
    logger.add(
        log_dir / "app-{time:YYYY-MM-DD}.log",
        level=level,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        encoding="utf-8",
        enqueue=True,
    )

    _CONFIGURED = True


def get_logger():
 # 获取全局日志记录器
    setup_logging()
    return logger