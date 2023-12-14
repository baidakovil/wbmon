# wbmon — Wildberries marketplace price monitor with Google Sheets publishing.
# Copyright (C) 2023 Ilia Baidakov <baidakovil@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <https://www.gnu.org/licenses/>.
"""This file contains function to save results into csv file."""

import logging
import os
from typing import List

from config import Cfg
from parsing.wbparser import PageResult

CFG = Cfg(test=os.getenv('TEST') == 'true')
logger = logging.getLogger('A.GC')
logger.setLevel(logging.DEBUG)


def save_values(full_result: List[PageResult]) -> None:
    """
    Function to save results into text file. Creates, if not exist.
    Args:
        full_result: parsed data
    """
    header_vars = [name.lower() for name in CFG.DATA_HEADER]
    try:
        open(CFG.STORING_CSV_FILENAME)
    except FileNotFoundError:
        with open(CFG.STORING_CSV_FILENAME, 'a') as file:
            file.write(CFG.STORING_CSV_SEPARATOR.join(header_vars))
            file.write('\n')
    with open(CFG.STORING_CSV_FILENAME, 'a') as file:
        for result in full_result:
            result_list = [str(result._asdict()[name]) for name in header_vars]
            result_list.append('\n')
            file.write(CFG.STORING_CSV_SEPARATOR.join(result_list))
    logger.info('Data saved to file: %s', CFG.STORING_CSV_FILENAME)
