from __future__ import annotations

from typing import Protocol

from .types import Data


class Serializable(Protocol):
  """
    Protocol for serializable objects. Classes implementing this protocol
    should provide a `serialize` method that returns data in a serialized format.

    Returns:
        SerializedData: The serialized representation of the object.
    """

  def serialize(self) -> Data:
    ...


class Deserializable(Protocol):
  """
    Protocol for deserializable objects. Classes implementing this protocol
    should provide a `deserialize` method that can construct the object from 
    serialized data.

    Args:
        data (SerializedData): The serialized input data from which to reconstruct the object.
    """

  def deserialize(self, data: Data):
    ...


class Serialization(Serializable, Deserializable, Protocol):
  """
    Protocol that combines both Serializable and Deserializable protocols.
    Classes implementing this protocol should be able to serialize their 
    state to a `SerializedData` format and reconstitute an object from it.
    """
  ...
