import logging, os
from utils.path_tool import get_abs_path
from datetime import datetime

# 日志保存根目录
LOG_ROOT = get_abs_path("logs")

# 确保日志的根目录
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式配置  ERROR=40  WARNING=30  INFO=20  DEBUG=10  NOTSET=0
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

def get_logger(
        name:str = "agent",
        console_level: int = logging.INFO,      # 控制台级别
        file_level: int = logging.DEBUG,        # 文件级别
        log_file = None
) -> logging.Logger:
    # 创建一个logger对象，里面包含两个Handler 一个是 console_handler 另一个是 file_handler
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 控制台的 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)                 # 控制台的级别
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)        # 使用什么格式

    logger.addHandler(console_handler)

    # 文件 Handler
    if not log_file:
        # 日志文件的存放路径
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger

# 快捷获取日志器
logger = get_logger()

if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")