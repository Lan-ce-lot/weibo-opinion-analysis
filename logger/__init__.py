# from rich import logging
import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)
StreamLogger = logging.getLogger("rich")

# logging.config.dictConfig(configs)
# StreamLogger = logging.getLogger("StreamLogger")
# FileLogger = logging.getLogger("FileLogger")
# 省略日志输出
StreamLogger.info("rich logger")
