# -*- coding: utf-8 -*-
import sys

from loguru import logger

_author_ = 'luwt'
_date_ = '2022/5/24 12:25'


# 移除原本的控制台输出样式
logger.remove()
log_format = (
    '<g>{time:YYYY-MM-DD HH:mm:ss SSS}</g> '
    '| <level>{level: <8}</level> '
    '| <e>{thread.name: <12}</e> '
    '| <cyan>{name}</cyan>: <cyan>{function}</cyan>: <cyan>{line}</cyan> '
    '- <level>{message}</level>'
)

# 定义新的控制台输出样式
if sys.stderr:
    logger.add(sys.stderr, format=log_format, level="INFO")


log_filename = "generator.log"
error_log_filename = "generator_error.log"
# 定义日志文件输出样式
logger.add(
    log_filename,
    format=log_format,
    level="DEBUG",
    rotation="100 MB",
)
# 定义错误日志文件输出样式
logger.add(
    error_log_filename,
    format=log_format,
    level="ERROR",
    rotation="100 MB"
)

