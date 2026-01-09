import datetime
import logging
import os.path

from sdk.logtools import clogger

_fmt = '%(asctime)s | %(name)s:%(levelname)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'


def _logger() -> logging.Logger:
    lg = clogger('KONO天猫', fmt=_fmt)
    folder = 'D:/reptile/download/konotm/log'
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, f'[{datetime.date.today()}].log')
    handler = logging.FileHandler(path)
    handler.setFormatter(logging.Formatter(_fmt))
    lg.addHandler(handler)
    return lg


logger = _logger()
