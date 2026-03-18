

class xint(int):
  """A class to extend the functionality of the built-in int class."""  
  def __new__(cls, value: int):
    x = int.__new__(cls, value)
    return x

  def __init__(self, value: int):
    if not isinstance(value, int):
      raise TypeError("xint must be an int")
    self._value =  value

  @property
  def ordinal(self) -> str:
    """Returns the ordinal representation of the number."""
    if 11 <= (self % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(self % 10, 4)]

    return f"{self}{suffix}"

  
    