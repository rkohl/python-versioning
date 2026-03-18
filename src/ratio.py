
class Ratio[T: float|int]:
  """
  A class to represent a ratio of two numbers.  
  """

  def __init__(self, numerator: T, denominator: T, precision: int = 1):
    """
    Initializes the Ratio object with a numerator and denominator.
    """
    self._numerator: T = numerator
    self._denominator: T = denominator
    self._precision: int = precision
    
  @property
  def numerator(self) -> T:
    """ Returns the numerator of the ratio."""
    return self._numerator

  @property
  def denominator(self) -> T:
    """ Returns the denominator of the ratio."""
    return self._denominator

  def __call__(self) -> str:
    return self.ratio
  
  @property
  def ratio(self) -> str:
    """
    Calculates the ratio of two numbers and returns the ratio as a string, the value as a float, and the numerator and denominator as integers.
    """
    
    if self.numerator == 0 or self.denominator == 0:
      return "0:0"

    from fractions import Fraction
    f1, f2 = round(self.numerator), round(self.denominator)
    ratio = Fraction(f1, f2).limit_denominator(10)
  
    return f"{ratio.numerator}:{ratio.denominator}"


  @property
  def value(self) -> float:
    """ Returns the ratio as a float."""
    return round(float(self.numerator) / float(self.denominator), self._precision)
    