from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TimeRemaining:
  """
  A class to represent the time remaining until a future date and time.
  """
  
  future: datetime
  seconds: float
  minutes: float
  hours: float
  days: float
  weeks: float
  months: float
  years: float
  formatted: str

  def __init__(self, future: datetime):
    future = future   
    now = datetime.now(tz=future.tzinfo)
    time_elapsed = future - now
    total_seconds = time_elapsed.total_seconds()
    
    # Calculate all units
    seconds = round(total_seconds, 1)
    minutes = round(seconds / 60, 1)
    hours = round(minutes / 60, 1)
    days = round(hours / 24, 1)
    weeks = round(days / 7, 1)
    months = round(days / 30, 1)
    years = round(days / 365, 1)
    
    parts = []
    remaining = total_seconds
    
    if years >= 1:
      years_int = int(years)
      parts.append(f"{years_int}yr")
      remaining -= years_int * 365 * 24 * 60 * 60
    
    if months >= 1 and remaining > 0:
      months_int = int(remaining / (30 * 24 * 60 * 60))
      if months_int > 0:
        parts.append(f"{months_int}m")
        remaining -= months_int * 30 * 24 * 60 * 60
    
    if weeks >= 1 and remaining > 0:
      weeks_int = int(remaining / (7 * 24 * 60 * 60))
      if weeks_int > 0:
        parts.append(f"{weeks_int}wk")
        remaining -= weeks_int * 7 * 24 * 60 * 60
    
    if days >= 1 and remaining > 0:
      days_int = int(remaining / (24 * 60 * 60))
      if days_int > 0:
        parts.append(f"{days_int}d")
        remaining -= days_int * 24 * 60 * 60
    
    if hours >= 1 and remaining > 0:
      hours_int = int(remaining / (60 * 60))
      if hours_int > 0:
        parts.append(f"{hours_int}hr")
        remaining -= hours_int * 60 * 60
    
    if minutes >= 1 and remaining > 0:
      minutes_int = int(remaining / 60)
      if minutes_int > 0:
        parts.append(f"{minutes_int}min")
        remaining -= minutes_int * 60
    
    if seconds >= 1 and remaining > 0:
      seconds_int = int(remaining)
      if seconds_int > 0:
        parts.append(f"{seconds_int}s")
    
    formatted = " ".join(parts) if parts else "0s"
    
    object.__setattr__(self, 'future', future)
    object.__setattr__(self, 'seconds', seconds)
    object.__setattr__(self, 'minutes', minutes)
    object.__setattr__(self, 'hours', hours)
    object.__setattr__(self, 'days', days)
    object.__setattr__(self, 'weeks', weeks)
    object.__setattr__(self, 'months', months)
    object.__setattr__(self, 'years', years)
    object.__setattr__(self, 'formatted', formatted)
