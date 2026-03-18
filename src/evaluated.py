from typing import Generic, TypeVar

T = TypeVar("T")  # Result type

class Evaluated(Generic[T]):
  """A class to represent an evaluated value."""
  def __init__(self, source):
      self._source = source

  @property
  def value(self) -> T:
      return self._source.evaluate()