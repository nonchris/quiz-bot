from datetime import datetime
from typing import Union

import dateparser


def parse_datetime(date_string: str) -> Union[datetime, None]:
    return dateparser.parse(date_string, languages=["de", "en"])


def isolate_date(date: datetime) -> Union[datetime, None]:
    """ Get rid of day time, just have the date - returns None when None is passed """
    return date.replace(hour=0, minute=0, second=0, microsecond=0) if date else None


def isolate_time(date: datetime) -> Union[datetime, None]:
    """ Unify date, just have the time - returns None when None is passed """
    return date.replace(year=1970, month=1, day=1) if date else None


def year_verification(guess: str, answer: str) -> bool:
    """ Verify guess and correct year """
    date = parse_datetime(guess)
    return str(date.year) == answer if date else False


def date_verification(guess: str, answer: str) -> bool:
    """ Verify a date ignore time """
    answer_date = isolate_date(parse_datetime(answer))
    guess_date = isolate_date(parse_datetime(guess))
    return answer_date == guess_date


def time_verification(guess: str, answer: str) -> bool:
    """ Verify a time, ignore date"""
    answer_date = isolate_time(parse_datetime(answer))
    guess_date = isolate_time(parse_datetime(guess))
    return answer_date == guess_date

