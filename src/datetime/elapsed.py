from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TimeSince:
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
