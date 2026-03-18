import re

class CleanPath:
  """Cleans a path by removing parameter names from path parameters."""

  PARAM_PATTERN = re.compile(r"<[^:>]+:([^>]+)>")

  @staticmethod
  def clean(path: str) -> str:
    cleaned = CleanPath.PARAM_PATTERN.sub(r"\1", path)
    return cleaned if cleaned else "/"