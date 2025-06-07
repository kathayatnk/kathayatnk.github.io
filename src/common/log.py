import inspect
import logging
import os
import sys

from asgi_correlation_id import correlation_id
from loguru import logger
from src.core.path_config import path_config
from src.core.settings import settings

class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class Log:
    def register(self) -> None:
        self._setup_logging()
        self._set_custom_logfile()

    @staticmethod
    def debug(msg: str, *args, **kwargs):
        logger.debug(msg, *args, **kwargs)
    
    @staticmethod
    def info(msg: str, *args, **kwargs):
        logger.info(msg, *args, **kwargs)
    
    @staticmethod
    def warning(msg: str, *args, **kwargs):
        logger.warning(msg, *args, **kwargs)
    
    @staticmethod
    def error(msg: str, *args, **kwargs):
        logger.error(msg, *args, **kwargs)
    
    @staticmethod
    def critical(msg: str, *args, **kwargs):
        logger.critical(msg, *args, **kwargs)
    
    @staticmethod
    def exception(msg: str, *args, **kwargs):
        logger.exception(msg, *args, **kwargs)


    def _setup_logging(self) -> None:
        logging.root.handlers = [InterceptHandler()]
        logging.root.setLevel(settings.LOG_STD_LEVEL)

        for name in logging.root.manager.loggerDict.keys():
            logging.getLogger(name).handlers = []
            if 'uvicorn.access' in name or 'watchfiles.main' in name:
                logging.getLogger(name).propagate = False
            else:
                logging.getLogger(name).propagate = True

        def correlation_id_filter(record):
            cid = correlation_id.get(settings.LOG_CID_DEFAULT_VALUE)
            record['correlation_id'] = cid[: settings.LOG_CID_UUID_LENGTH]
            return record

        logger.remove() 
        logger.configure(
            handlers=[
                {
                    'sink': sys.stdout,
                    'level': settings.LOG_STD_LEVEL,
                    'filter': lambda record: correlation_id_filter(record),
                    'format': settings.LOG_STD_FORMAT,
                }
            ]
        )


    def _set_custom_logfile(self) -> None:
        log_path = path_config.log_dir
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        log_access_file = os.path.join(log_path, settings.LOG_ACCESS_FILENAME)
        log_error_file = os.path.join(log_path, settings.LOG_ERROR_FILENAME)

        log_config = {
            'format': settings.LOG_FILE_FORMAT,
            'enqueue': True,
            'rotation': '5 MB',
            'retention': '7 days',
            'compression': 'tar.gz',
        }

        logger.add(
            str(log_access_file),
            level=settings.LOG_ACCESS_FILE_LEVEL,
            filter=lambda record: record['level'].no <= 25,
            backtrace=False,
            diagnose=False,
            **log_config,
        )

        logger.add(
            str(log_error_file),
            level=settings.LOG_ERROR_FILE_LEVEL,
            filter=lambda record: record['level'].no >= 30,
            backtrace=True,
            diagnose=True,
            **log_config,
        )


log = Log()
