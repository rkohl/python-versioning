from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias, Union
from datetime import datetime


JSON: TypeAlias = Union[
    dict[str, "JSON"],
    list["JSON"],
    str,
    int,
    float,
    bool,
    None,
]
"""
Type alias for JSON data. This is a recursive type that can represent any valid JSON value.
It includes dictionaries, lists, strings, numbers, booleans, and None.
"""

Data: TypeAlias = Union[
    dict[str, "Data"],
    list["Data"],
    str,
    int,
    float,
    bool,
    datetime,
    None,
]
"""
Type alias for data that can be serialized. This is similar to JSON but includes additional types
like datetime and bytes.
"""


ModeledData: TypeAlias = Data
"""
Type alias for modeled data. This is the same as Data but is used to distinguish between raw data
and modeled data.
"""


RawJSON: TypeAlias = JSON
"""
Type alias for raw JSON data. This is the same as JSON but is used to distinguish between raw JSON
data and modeled data.
"""