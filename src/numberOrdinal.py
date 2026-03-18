
class OrdinalNumber:
  """A class to represent an ordinal number."""

  def __new__(cls, number: int):
    return int.__new__(cls, number)

  def __init__(self, number: int):
    self._value = number

  @property
  def ordinal(self) -> str:
    """Returns the ordinal representation of the number."""
    if 11 <= (self._value % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(self._value % 10, 4)]
    return f"{self._value}{suffix}"

  def __str__(self) -> str:
    return self.ordinal

  def __repr__(self) -> str:
    return f"OrdinalNumber({self._value}-{self.ordinal})"

  @property
  def __call__(self):
    return self.ordinal
    
def numberOrdinal(number: int):
  if 11 <= (number % 100) <= 13:
      suffix = 'th'
  else:
      suffix = ['th', 'st', 'nd', 'rd', 'th'][min(number % 10, 4)]
  return str(number) + suffix