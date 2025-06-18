import logging

# 配置日志输出格式和级别（推荐格式）
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(process)d | %(threadName)s | %(name)s | %(filename)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='./logs/example.log',  # 日志写入文件
    encoding='utf-8',  # 确保日志文件编码为UTF-8
    filemode='a'  # 每次运行覆盖日志文件
)

# 控制台也输出日志，使用同样的格式
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(process)d | %(threadName)s | %(name)s | %(filename)s:%(lineno)d | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# 日志演示
logging.debug('这是一个DEBUG日志，调试信息')
logging.info('这是一个INFO日志，普通信息')
logging.warning('这是一个WARNING日志，警告信息')
logging.error('这是一个ERROR日志，错误信息')
logging.critical('这是一个CRITICAL日志，严重错误')

# 你可以在此基础上继续学习和实验 logging 的更多用法

# =========================
# 进阶1：日志分模块与多Logger管理
# =========================

# 创建一个新的logger，通常用于不同模块
module_logger = logging.getLogger('my_module')
module_logger.setLevel(logging.DEBUG)

# 为该logger单独添加一个handler（比如只输出到控制台）
module_console_handler = logging.StreamHandler()
module_console_handler.setLevel(logging.DEBUG)
module_console_handler.setFormatter(logging.Formatter('[my_module] %(levelname)s: %(message)s'))
module_logger.addHandler(module_console_handler)

# 使用不同logger输出日志
module_logger.debug('my_module 的 DEBUG 日志')
module_logger.info('my_module 的 INFO 日志')

# 你可以在不同文件/模块中用 logging.getLogger('模块名') 获取同名logger，实现分模块日志管理
# 例如：
# from logging import getLogger
# logger = getLogger('my_module')
# logger.info('跨文件同名logger会复用handler和配置')
