from __future__ import annotations

import re
from functools import total_ordering
from typing import TypeAlias
from itertools import zip_longest

SemVer: TypeAlias = str
SemVerList: TypeAlias = list[SemVer]
SemVers: TypeAlias = SemVerList | SemVer

_VERSION_REGEX = re.compile(
    r'^'
    r'(\d+)\.(\d+)\.(\d+)'  # major, minor, patch
    r'(-[0-9A-Za-z-\.]+)?'  # pre-release
    r'(\+[0-9A-Za-z-\.]+)?'  # build metadata
    r'$'
)


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
                    return s < o  # type: ignore[operator]
            else:
                return isinstance(s, int)
        return False


@total_ordering
class Version:
    """Represents a semantic version."""

    def __init__(self, version: SemVers):
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

    def _parse(self, version: SemVer) -> None:
        m = _VERSION_REGEX.match(version)
        if not m:
            raise VersionError(f'invalid version {version!r}')
        self.major, self.minor, self.patch = int(m[1]), int(m[2]), int(m[3])
        self.pre_release = _parse_group(m[4])
        self.build = _parse_group(m[5])

    def add(self, version: SemVer) -> None:
        """Add a version to the tracked list."""
        if version not in self._all_versions:
            if not _VERSION_REGEX.match(version):
                raise VersionError(f'invalid version {version!r}')
            self._all_versions.append(version)

    @property
    def latest(self) -> Version:
        """Return the latest version from the tracked list."""
        return max(self.versions)

    @property
    def version(self) -> SemVer:
        """Return the string representation of the version."""
        return str(self)

    @property
    def versions(self) -> list[Version]:
        """Return all tracked versions as Version objects."""
        return [Version(v) for v in self._all_versions]

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
