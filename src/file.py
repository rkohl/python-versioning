from pathlib import Path


class File:
  """Represents a file with its path and extension."""
  _file: Path

  def __init__(self, file: str | Path) -> None:
    if isinstance(file, str):
      file = Path(file)
    self._file = file

  @property
  def file(self) -> Path:
    """Returns the file path."""
    return self._file

  @property
  def filename(self) -> str:
    """Returns the file name as a string."""
    return self._file.as_posix()

  @property
  def ext(self) -> str:
    """Returns the file extension."""
    return self._file.suffix

  @property
  def name(self) -> str:
    """Returns the file name without the extension."""
    return self._file.name