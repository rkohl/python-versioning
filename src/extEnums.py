from enum import StrEnum, Enum, IntEnum
from typing import Any


class ExtEnum(Enum):
  """
  Extends the base Enum class to provide additional utility methods.
  """

  @classmethod
  def names(cls) -> list[str]:
    """
    Returns a list of the names of the enum members.
    """
    return [c.name for c in cls]

  @classmethod
  def values(cls):
    """
    Returns a list of the values of the enum members.
    """
    return [c.value for c in cls]

  @classmethod
  def commaSeperatedValues(cls) -> str:
    """
    Returns a comma-separated string of the values of the enum members.
    """
    return ','.join([str(c.value) for c in cls])

  @classmethod
  def keyValueDict(cls) -> dict[str, Any]:
    """
    Returns a dictionary of the enum members, where the keys are the 
     names and the values are the values.
    """
    return {c.name: c.value for c in cls}

  @classmethod
  def cases(cls):
    """
    Returns a list of the enum members.
    """
    return list(cls)


class ExtStrEnum(StrEnum):
  """
  Extends the base StrEnum class to provide additional utility methods.
  """

  @classmethod
  def names(cls) -> list[str]:
    """
    Returns a list of the names of the enum members.
    """
    return [c.name for c in cls]

  @classmethod
  def values(cls) -> list[str]:
    """
    Returns a list of the values of the enum members.
    """
    return [c.value for c in cls]

  @classmethod
  def commaSeperatedValues(cls) -> str:
    """
    Returns a comma-separated string of the values of the enum members.
    """
    return ','.join([c.value for c in cls])

  @classmethod
  def keyValueDict(cls) -> dict[str, str]:
    """
    Returns a dictionary of the enum members, where the keys are the 
     names and the values are the values.
    """
    return {c.name: c.value for c in cls}

  @classmethod
  def cases(cls) -> list[str]:
    """
    Returns a list of the enum members.
    """
    return list(cls)


class ExtIntEnum(IntEnum):
  """
  Extends the base IntEnum class to provide additional utility methods.
  """

  @classmethod
  def names(cls) -> list[str]:
    """
    Returns a list of the names of the enum members.
    """
    return [c.name for c in cls]

  @classmethod
  def values(cls):
    """
    Returns a list of the values of the enum members.
    """
    return [c.value for c in cls]

  @classmethod
  def commaSeperatedValues(cls) -> str:
    """
    Returns a comma-separated string of the values of the enum members.
    """
    return ','.join([str(c.value) for c in cls])

  @classmethod
  def keyValueDict(cls) -> dict[str, Any]:
    """
    Returns a dictionary of the enum members, where the keys are the 
     names and the values are the values.
    """
    return {c.name: c.value for c in cls}

  @classmethod
  def cases(cls):
    """
    Returns a list of the enum members.
    """
    return list(cls)
