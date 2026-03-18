def between[T: float|int](value: T, lower: T, upper: T):
  """Returns true if the value is between the lower and upper bounds"""
  return lower < value < upper

def betweenInclusive[T: float|int](value: T, lower: T, upper: T):
  """Returns true if the value is between the lower and upper bounds, inclusive"""
  return lower <= value <= upper
