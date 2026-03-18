from typing import List, Sequence

def splitList[T](list: List[T] | Sequence[T], size=10) -> List[List[T] | Sequence[T]]:
  return [list[i:i + size] for i in range(0, len(list), size)]