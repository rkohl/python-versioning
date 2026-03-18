import math
import decimal

def precision(value:float) -> int:
  """
  Returns the number of decimal places in a float.
  """

  if value == 0:
      return 0

  s = str(value)
  if '.' in s:
 
    return len(s.split('.')[1])
  else:
    return 0
