

class Progress[I: float|int, T: float|int]:
  """A class to represent a progress value with optional scaling and precision."""

  def __init__(self, progress: I, total: T, precision: int = 2):
    """Initialize the Progress object with a progress and total value, and precision."""
    self._progress = progress
    self._total = total
    self.precision = precision

  @property
  def progress(self) -> I:
    """ Returns the progress value."""
    return self._progress

  @property
  def total(self) -> T:
    """ Returns the total value."""
    return self._total

  @property
  def value(self) -> float:
    """ Returns the progress value."""
    if self.progress == 0 or self.total == 0:
      return 0
    return round(float(self.progress) / float(self.total), self.precision)

  @property
  def percent(self) -> float:
    """ Returns the progress value as a percentage."""
    if self.progress == 0 or self.total == 0:
      return 0
    return round(float(self.progress) / float(self.total) * 100, self.precision)

  def __call__(self) -> float:
    """ Returns the progress value."""
    return self.value

