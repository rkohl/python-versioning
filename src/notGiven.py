from __future__ import annotations
from typing import (Any, Dict, Literal, Mapping, TypeAlias, Union, override,
TypeVar, Optional)

_T = TypeVar("_T")


class NotGiven:
  """
    A sentinel singleton class used to distinguish omitted keyword arguments
    from those passed in with the value None (which may have different behavior).
    """

  def __bool__(self) -> Literal[False]:
    return False

  @override
  def __repr__(self) -> str:
    return "NOT_GIVEN"


NotGivenOr = Union[_T, NotGiven]
"""Type alias for a value that may be explicitly omitted."""

NOTGIVEN = NotGiven()
"""Singleton instance of NotGiven, used as a default for omitted arguments."""