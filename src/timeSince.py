from dataclasses import dataclass
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from typing import TypeAlias

Minutes: TypeAlias = int
Days: TypeAlias = int

@dataclass(frozen=True)
class TimeSince:
  """
  A class to represent the time elapsed since a given date and time.
  """
  since: datetime
  seconds: float
  minutes: float
  hours: float
  days: float
  weeks: float
  months: float
  years: float
  formatted: str

  def __init__(self, since: datetime):
    since = since   
    now = datetime.now(tz=since.tzinfo)
    time_elapsed = now - since
    seconds = round(time_elapsed.total_seconds(), 1)
    minutes = round(seconds / 60, 1)
    hours = round(minutes / 60, 1)
    days = round(hours / 24, 1)
    weeks = round(days / 7, 1)
    months = round(days / 30, 1)
    years = round(days / 365, 1)
    if years >= 1:
      formatted = f"{int(years)}yr ago"
    elif months >= 1:
      formatted = f"{int(months)}m ago"
    elif weeks >= 1:
      formatted = f"{int(weeks)}wk ago"
    elif days >= 1:
      formatted = f"{int(days)}d ago"
    elif hours >= 1:
      formatted = f"{int(hours)}hr ago"
    elif minutes >= 1:
      formatted = f"{int(minutes)}min ago"
    else:
      formatted = f"{int(seconds)}s ago"

    object.__setattr__(self, 'since', since)
    object.__setattr__(self, 'seconds', seconds)
    object.__setattr__(self, 'minutes', minutes)
    object.__setattr__(self, 'hours', hours)
    object.__setattr__(self, 'days', days)
    object.__setattr__(self, 'weeks', weeks)
    object.__setattr__(self, 'months', months)
    object.__setattr__(self, 'years', years)
    object.__setattr__(self, 'formatted', formatted)

  
  @classmethod
  def relativeMinutesFrom(cls, minutes: Minutes, tz: ZoneInfo = ZoneInfo('America/Chicago')):
    relative = datetime.now(tz=tz) - timedelta(minutes=minutes)
    return cls(relative)

  @classmethod
  def relativeDaysFrom(cls, days: Days, tz: ZoneInfo = ZoneInfo('America/Chicago')):
    relative = datetime.now(tz=tz) - timedelta(days=days)
    return cls(relative)
    