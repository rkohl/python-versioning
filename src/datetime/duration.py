from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

@dataclass
class Duration:
  """A class to represent a duration of time formated as smalled unit (s, m, hr, d)"""
  start: datetime
  end: datetime

  def __init__(self, start: datetime, end: datetime):
    if start > end:
      raise ValueError("Start time must be before end time")
    self.start = start
    self.end = end.replace(tzinfo=self.start.tzinfo)
    
    

  @property
  def seconds(self) -> float:
    """Returns the duration in seconds."""
    if self.start != self.end:
      return (self.end - self.start).total_seconds()
    return 0
    
  @property
  def formatted(self) -> str:
    """Returns the duration formatted as the smallest unit of time required."""
    total_seconds = self.seconds
    
    # Convert to days
    if total_seconds >= 86400:  # 60 * 60 * 24
      days = total_seconds / 86400
      return f"{days:.1f}d" if days % 1 != 0 else f"{int(days)}d"
    
    # Convert to hours
    if total_seconds >= 3600:  # 60 * 60
      hours = total_seconds / 3600
      return f"{hours:.1f}hr" if hours % 1 != 0 else f"{int(hours)}hr"
    
    # Convert to minutes
    if total_seconds >= 60:
      minutes = total_seconds / 60
      return f"{minutes:.1f}m" if minutes % 1 != 0 else f"{int(minutes)}m"
    
    # Return as seconds
    return f"{total_seconds:.1f}s" if total_seconds % 1 != 0 else f"{int(total_seconds)}s"