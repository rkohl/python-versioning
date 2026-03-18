import json


def prettyPrint(data, sort=False) -> None:
  """
  Prints dictionaries in a pretty format
  """
  print(json.dumps(data, sort_keys=sort, indent=2, separators=(',', ': ')))