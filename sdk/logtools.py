# -*- coding: utf-8 -*-  
"""
@Date     : 2024-08-16
@Author   : xwq
@Desc     : <None>

"""
import logging
import typing

import colorlog


_FMT = '%(asctime)s|%(name)s:%(levelname)s|%(filename)s:%(lineno)d|%(funcName)s|%(message)s'


def colorfy(logger: logging.Logger, fmt: str = _FMT,) -> logging.Logger:
    """
    使日志器的控制台输出具备颜色区分
    :param logger:
    :param fmt:
    :return:
    """
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        f'%(log_color)s{fmt}',
        log_colors={
            'DEBUG': 'green',
            'INFO': 'blue',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    ))
    logger.addHandler(handler)
    return logger


def filefy(
        logger: logging.Logger,
        builder: typing.Callable,
        fmt: str = _FMT,
        *args,
        **kwargs,
) -> logging.Logger:
    """
    使日志器记录文件中，文件位置由builder生成
    :param logger:
    :param builder:
    :param fmt:
    :param args:
    :param kwargs:
    :return:
    """
    path = builder(*args, **kwargs)
    handler = logging.FileHandler(path)
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger


def clogger(name: str = 'clogger', level: int = logging.INFO, fmt: str = _FMT) -> logging.Logger:
    """
    生成一个控制台输出有色的logger
    :param name:
    :param level:
    :param fmt:
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    colorfy(logger, fmt)
    return logger
