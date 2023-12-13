# wbmon — Wildberries marketplace price monitor with Google Sheets publishing.
# Copyright (C) 2021-2023 Ilia Baidakov <baidakovil@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <https://www.gnu.org/licenses/>.
"""This file contains advanced function to generate logging.Logger logger."""

import logging
import os
from logging.handlers import RotatingFileHandler

from config import Cfg

CFG = Cfg(test=os.getenv('TEST') == 'true')


def start_logger() -> logging.Logger:
    """
    Returns logging.Logger from nothing. Loggers definition. Logger in logger.py is the
    highest (A), other are descendants: A.ma, A.gc, etc.
    """
    logger = logging.getLogger('A')
    logger.setLevel(logging.DEBUG)

    class ContextFilter(logging.Filter):
        """
        Necessary for escaping messages in console with large data (URLs, ...), but log
        it in rotating handler.
        """

        def filter(self, record):
            if CFG.LOGGER_FILTER_MSG in record.msg:
                return 0
            else:
                return 1

    #  Logging to console.
    ch = logging.StreamHandler()
    #  Logging to file since last run (debugging case).
    fh = logging.FileHandler(filename=os.path.join('logger.log'), mode='w')
    #  Logging to file, continuous after bot restart.
    rh = RotatingFileHandler(
        filename=os.path.join(CFG.PATH_LOGGER, CFG.FILE_ROTATING_LOGGER),
        mode='a',
        maxBytes=CFG.BYTES_MAX_ROTATING_LOGGER,
        backupCount=CFG.QTY_BACKUPS_ROTATING_LOGGER,
    )
    ch_formatter = logging.Formatter(
        '[%(asctime)s.%(msecs)03d - %(name)3s - %(levelname)8s - %(funcName)18s()] %(message)s',
        '%H:%M:%S',
    )
    fh_formatter = logging.Formatter(
        '[%(asctime)s.%(msecs)03d - %(name)20s - %(filename)20s:%(lineno)4s - %(funcName)20s() - %(levelname)8s - %(threadName)10s] %(message)s',
        '%Y-%m-%d %H:%M:%S',
    )
    ch.setLevel(logging.DEBUG)
    rh.setLevel(logging.DEBUG)
    ch.setFormatter(ch_formatter)
    rh.setFormatter(fh_formatter)
    logger.addHandler(ch)
    logger.addHandler(rh)
    ch_filter = ContextFilter()
    ch.addFilter(ch_filter)
    return logger


logger = start_logger()
logger.info('Main logger started, __name__ is %s', __name__)
