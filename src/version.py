from __future__ import annotations

import re
from functools import total_ordering
from itertools import zip_longest

_VERSION_REGEX = re.compile(
    r'^'
    r'(\d+)\.(\d+)\.(\d+)'  # major, minor, patch
    r'(-[0-9A-Za-z-\.]+)?'  # pre-release
    r'(\+[0-9A-Za-z-\.]+)?'  # build metadata
    r'$'
)


MAJOR = 'major'
MINOR = 'minor'
PATCH = 'patch'
BUILD = 'build'


class VersionError(Exception):
    """Exception raised for invalid version strings."""


def _try_int(s: str) -> int | str:
    try:
        return int(s)
    except ValueError:
        return s


def _parse_group(g: str | None) -> list[int | str]:
    return [] if g is None else [_try_int(x) for x in g[1:].split('.')]


@total_ordering
class _Seq:
    """Sequence of identifiers comparable according to SemVer rules."""

    def __init__(self, seq: list[int | str]):
        self.seq = seq

    def __eq__(self, other: object) -> bool:
        return self.seq == other.seq  # type: ignore[attr-defined]

    def __lt__(self, other: _Seq) -> bool:
        for s, o in zip_longest(self.seq, other.seq):
            if s is None or o is None:
                return s is None
            if type(s) is type(o):
                if s != o:
                    return s < o
            else:
                return isinstance(s, int)
        return False


@total_ordering
class Version:
    """Represents a semantic version."""

    def __init__(self, version: str | list[str]):
        self._all_versions: list[str] = []

        if isinstance(version, list):
            if not version:
                raise VersionError('No versions provided in the list')
            self._all_versions = [v for v in version if _VERSION_REGEX.match(v)]
            if not self._all_versions:
                raise VersionError('No valid versions found in the list')
            self._parse(max(Version(v) for v in self._all_versions).version)
        else:
            self._parse(version)
            self._all_versions.append(version)

    def add(self, version: str) -> None:
      """Add a version to the tracked list."""
      
      if version not in self._all_versions:
        if not _VERSION_REGEX.match(version):
            raise VersionError(f'invalid version {version!r}')
        self._all_versions.append(version)
        if Version(version) > Version(str(self)):
          self._parse(max(Version(v) for v in self._all_versions).version)

    def remove(self, version: str) -> None:
      """Remove a version from the tracked list."""
      
      if version not in self._all_versions:
        raise VersionError(f'Version {version!r} not found in tracked versions')
        
      if len(self.versions) <= 1:
        raise VersionError('Cannot remove this version')
      elif version == str(self):
        self._all_versions.remove(version)
        self._parse(self.latest)
      else:
        self._all_versions.remove(version)

    
    def increment(self, part: str) -> None:
        """Increment major, minor, patch, or build using the MAJOR, MINOR, PATCH, or BUILD constants."""
        if part == MAJOR:
            new_version = f'{self.major + 1}.0.0'
        elif part == MINOR:
            new_version = f'{self.major}.{self.minor + 1}.0'
        elif part == PATCH:
            new_version = f'{self.major}.{self.minor}.{self.patch + 1}'
        elif part == BUILD:
            new_version = self._next_build()
        else:
            raise ValueError(f'invalid part {part!r}: use MAJOR, MINOR, PATCH, or BUILD')
        self._all_versions.append(new_version)
        self._parse(new_version)

    def _next_build(self) -> str:
        """Return a new version string with the build metadata incremented."""
        mmp = f'{self.major}.{self.minor}.{self.patch}'
        pre = '-' + '.'.join(str(c) for c in self.pre_release) if self.pre_release else ''

        if not self.build:
            return f'{mmp}{pre}+b1'

        parts = list(self.build)
        last = parts[-1]

        if isinstance(last, int):
            parts[-1] = last + 1
        else:
            m = re.match(r'^(.*?)(\d+)$', last)
            if m:
                parts[-1] = m.group(1) + str(int(m.group(2)) + 1)
            else:
                parts.append(1)

        return f'{mmp}{pre}+{".".join(str(x) for x in parts)}'

    @property
    def latest(self) -> str:
        """Return the latest version from the tracked list."""
        return max(self.versions).version

    @property
    def version(self) -> str:
        """Return the string representation of the version."""
        return str(self)

    @property
    def versions(self) -> list[Version]:
        """Return all tracked versions as Version objects sorted descending."""
        return sorted([Version(v) for v in self._all_versions], reverse=True)

    def __str__(self) -> str:
        s = f'{self.major}.{self.minor}.{self.patch}'
        if self.pre_release:
            s += '-' + '.'.join(str(c) for c in self.pre_release)
        if self.build:
            s += '+' + '.'.join(str(c) for c in self.build)
        return s

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({str(self)!r})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            raise TypeError(f'cannot compare {self!r} with {other!r}')
        return (
            (self.major, self.minor, self.patch, self.pre_release, self.build) ==
            (other.major, other.minor, other.patch, other.pre_release, other.build)
        )

    def __lt__(self, other: Version) -> bool:
        if not isinstance(other, Version):
            raise TypeError(f'cannot compare {self!r} with {other!r}')
        if (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch):
            return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
        if self.pre_release != other.pre_release:
            if self.pre_release and other.pre_release:
                return _Seq(self.pre_release) < _Seq(other.pre_release)
            return bool(self.pre_release)
        if self.build != other.build:
            if self.build and other.build:
                return _Seq(self.build) < _Seq(other.build)
            return bool(self.build)
        return False

    def _parse(self, version: str) -> None:
      m = _VERSION_REGEX.match(version)
      if not m:
          raise VersionError(f'invalid version {version!r}')
      self.major, self.minor, self.patch = int(m[1]), int(m[2]), int(m[3])
      self.pre_release = _parse_group(m[4])
      self.build = _parse_group(m[5])
