import math
import decimal

class pfloat(float):
  """A float with a precision property."""
  
  def __new__(cls, value: float):
    if not isinstance(value, float):
      raise TypeError("pfloat must be a float")
    return super().__new__(cls, value)

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


def precision(value:float) -> int:
  """
  Returns the number of decimal places in a float.
  """

  if value == 0:
      return 0

  abs_num = abs(value)
  if abs_num < 0.0001:
      # Count leading zeros after decimal
      exponent = int(math.floor(math.log10(abs_num)))
      return abs(exponent) + 3
  else:
    exponent = decimal.Decimal(str(value)).as_tuple().exponent
    if isinstance(exponent, int):
      p = abs(exponent)
    return 0