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
"""This is the main program file: loading logger, environment, running the scheduler."""

import logging

from dotenv import load_dotenv

from parsing.scheduler import get_scheduler
from services.logger import logger

load_dotenv('.env')

logger = logging.getLogger('A.ma')
logger.setLevel(logging.DEBUG)


def main() -> None:
    """
    Function to run monitoring. Opa.
    """
    scheduler = get_scheduler()
    try:
        logger.info('Program run now')
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
