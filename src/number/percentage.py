

class Percentage:
  """A class to represent a percentage value with optional scaling and precision."""

  def __init__(self, value: float, shouldScale: bool = False, precision: int = 2):
    """Initialize the Percentage object with a value, optional scaling, and precision."""
    self.shouldScale = shouldScale
    self._scale = 100 if self.shouldScale else 1
    self._raw = value
    self.precision = precision

  
  @property
  def value(self) -> float:
    """ Returns the percentage value."""
    return round(self._raw * self._scale, self.precision)

  @property
  def raw(self) -> float:
    """ Returns the raw value."""
    return self._raw

  @property
  def scale(self) -> float:
    """ Returns the scale value."""
    return self._scale

  def __call__(self) -> str:
    """ Returns the percentage value."""
    return self.percent
    
  @property
  def percent(self) -> str:
    """ Returns the percentage value as a string with a '%' symbol."""
    return f"{self.value}%"

  @property
  def decimal(self) -> float:
     """ Returns the percentage value as a decimal."""
     return self.value / 100

  @property
  def fraction(self) -> str:
      """ Returns the percentage value as a fraction."""
      return f"{self.value}/100"