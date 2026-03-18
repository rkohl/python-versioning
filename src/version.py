from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TypeAlias
from itertools import zip_longest

Semantic: TypeAlias = str
SemanticList: TypeAlias = list[Semantic]
Semantics: TypeAlias = SemanticList | Semantic

_VERSION_REGEX = re.compile(
    r'^'
    r'(\d+)\.(\d+)\.(\d+)'  # major, minor, patch
    r'(-[0-9A-Za-z-\.]+)?'  # pre-release
    r'(\+[0-9A-Za-z-\.]+)?'  # build metadata
    r'$'
)


class VersionError(Exception):
    """Exception raised for invalid version strings."""
    pass


class _Comparable:
    """Rich comparison operators based on __lt__ and __eq__."""

    def __gt__(self, other):
        return not self < other and not self == other

    def __le__(self, other):
        return self < other or self == other

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return self > other or self == other


class _Seq(_Comparable):
    """Sequence of identifiers that can be compared according to semver."""

    def __init__(self, seq):
        self.seq = seq

    def __lt__(self, other):
        assert set([int, str]) >= set(map(type, self.seq))
        for s, o in zip_longest(self.seq, other.seq):
            assert not (s is None and o is None)
            if s is None or o is None:
                return bool(s is None)
            if type(s) is int and type(o) is int:
                if s < o:
                    return True
            elif type(s) is int or type(o) is int:
                return type(s) is int
            elif s != o:
                return s < o

    def __eq__(self, other):
        return self.seq == other.seq


def _try_int(s: str) -> int | str:
    """Convert string to int if possible, otherwise return string."""
    try:
        return int(s)
    except ValueError:
        return s


def _make_group(g: str | None) -> list[int | str]:
    """Parse a semver group (pre-release or build metadata)."""
    return [] if g is None else list(map(_try_int, g[1:].split('.')))


class Version(_Comparable):
    """Represents a semantic version."""

    def __init__(self, version: Semantics):
      self._all_versions: list[str] = []

      if isinstance(version, list):
        if len(version) == 0:
          raise VersionError('No versions provided in the list')
      
        self._all_versions = [str(v) for v in version if _VERSION_REGEX.match(v)]
        if not self._all_versions:
          raise VersionError('No valid versions found in the list')
          
        latest_version = max([Version(v) for v in self._all_versions], key=lambda v: (v.major, v.minor, v.patch))
        self._set_version(latest_version.version)

      else:
        self._set_version(version)

    def _set_version(self, version: Semantic) -> None:
        checked = self._check(version)
        self.major, self.minor, self.patch = map(int, checked.groups()[:3])
        self.pre_release = _make_group(checked.group(4))
        self.build = _make_group(checked.group(5))

    def _check(self, version: Semantic) -> re.Match:
        """Validate version string and return regex match."""
        match = _VERSION_REGEX.match(version)
        if not match:
          raise VersionError(f'invalid version {version!r}')
        return match

    def add(self, version: Semantic) -> None:
        """Add a version to the list of tracked versions."""
        if version not in self._all_versions and self._check(version):
            self._all_versions.append(version)

    @property
    def latest(self) -> Version:
        """Return the latest version from the tracked versions."""
        if not self._all_versions:
            return self
        sorted_versions = sorted(self._all_versions, reverse=True)
        return Version(sorted_versions[0])

    @property
    def version(self) -> Semantic:
        """Return the string representation of the version."""
        return str(self)

    @property
    def versions(self) -> list[Version]:
        """Return all tracked versions as Version objects."""
        return [Version(v) for v in self._all_versions]

    def __str__(self) -> str:
        s = '.'.join(str(c) for c in self._mmp())
        if self.pre_release:
            s += f"-{'.'.join(str(c) for c in self.pre_release)}"
        if self.build:
            s += f"+{'.'.join(str(c) for c in self.build)}"
        return s

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({str(self)!r})'

    def _mmp(self) -> list[int]:
        """Return major, minor, patch as a list."""
        return [self.major, self.minor, self.patch]

    def __lt__(self, other) -> bool:
        self._assume_to_be_comparable(other)

        if self._mmp() != other._mmp():
            return self._mmp() < other._mmp()

        if self.pre_release != other.pre_release:
            if self.pre_release and other.pre_release:
                return _Seq(self.pre_release) < _Seq(other.pre_release)
            return bool(self.pre_release)

        if self.build != other.build:
            if self.build and other.build:
                return _Seq(self.build) < _Seq(other.build)
            return bool(self.build)

        return False

    def __eq__(self, other) -> bool:
        self._assume_to_be_comparable(other)
        return (self._mmp() == other._mmp() and
                self.build == other.build and
                self.pre_release == other.pre_release)

    def _assume_to_be_comparable(self, other) -> None:
        """Ensure other is a Version instance for comparison."""
        if not isinstance(other, Version):
            raise TypeError(f'cannot compare {self!r} with {other!r}')
