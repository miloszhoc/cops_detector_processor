import datetime

from utils.logs import LOGGER


def validate_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        LOGGER.error('Invalid date format: {}'.format(date_string))
        return False


