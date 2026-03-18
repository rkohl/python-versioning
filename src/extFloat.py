from __future__ import annotations
import math
import decimal
from .progress import Progress

class xfloat(float):
  """A float with a precision property."""

  def __new__(cls, value):
    x = float.__new__(cls, value)
    return x

  def __init__(self, value):
    if not isinstance(value, float):
      raise TypeError("xfloat must be a float")
    self._value = value
    
  @property
  def precision(self) -> int:
    """Returns the number of decimal places."""
    if self == 0:
      return 0

    abs_num = abs(self)
    if abs_num < 0.0001:
        exponent = int(math.floor(math.log10(abs_num)))
        return abs(exponent) + 3
    else:
      exponent = decimal.Decimal(str(self)).as_tuple().exponent
      if isinstance(exponent, int):
        p = abs(exponent)
      return 0

  @property
  def fraction(self) -> str:
    import fractions
    """Returns the float as a fraction."""
    fract = fractions.Fraction(self)
    return f"{fract.numerator}:{fract.denominator}"

  def between[T: float|xfloat](self, lower: T, upper: T):
    """Returns true if the value is between the lower and upper bounds"""
    return lower < self < upper

  def greaterThan[T: float|xfloat](self, value: T) -> bool:
    """Returns true if the value is greater than the given value"""
    return self > value

  def lessThan[T: float|xfloat](self, value: T) -> bool:
    """Returns true if the value is less than the given value"""
    return self < value

  def percentage[T: float|xfloat|int](self, total: T, precision: int = 2) -> xfloat:
    """Returns the progress value."""
    if total == 0:
      return xfloat(0)
    return xfloat(round(self/total, precision))

  def progress(self, total: float|int, precision: int = 2) -> Progress:
    """Returns the progress value."""
    return Progress(float(self), total, precision)
    
  def __add__(self, other):
    if isinstance(other, xfloat):
      return xfloat(float(self) + float(other))
    if  isinstance(other, float):
      return xfloat(float(self) + other)
    if isinstance(other, int):
      return xfloat(float(self) + float(other))
      
  def __sub__(self, other):
    if isinstance(other, xfloat):
      return xfloat(float(self) - float(other))
    if  isinstance(other, float):
      return xfloat(float(self) - other)
    if isinstance(other, int):
      return xfloat(float(self) - float(other))

  def __mul__(self, other):
    if isinstance(other, xfloat):
      return xfloat(float(self) * float(other))
    if  isinstance(other, float):
      return xfloat(float(self) * other)
    if isinstance(other, int):
      return xfloat(float(self) * float(other))

  def __truediv__(self, other):
    if isinstance(other, xfloat):
      return xfloat(float(self) / float(other))
    if  isinstance(other, float):
      return xfloat(float(self) / other)
    if isinstance(other, int):
      return xfloat(float(self) / float(other))

  def  __floordiv__(self, other):
    if isinstance(other, xfloat):
      return xfloat(float(self) // float(other))
    if  isinstance(other, float):
      return xfloat(float(self) // other)
    if isinstance(other, int):
      return xfloat(float(self) // float(other))

  def __mod__(self, other):
    if isinstance(other, xfloat):
      return xfloat(float(self) % float(other))
    if  isinstance(other, float):
      return xfloat(float(self) % other)
    if isinstance(other, int):
      return xfloat(float(self) % float(other))
