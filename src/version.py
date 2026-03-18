from __future__ import print_function, annotations
import sys
import re
from dataclasses import dataclass
from typing import List, Self, TypeAlias

if sys.version_info >= (3, 0):
  from itertools import zip_longest as izip_longest
else:
  from itertools import izip_longest

Semantic: TypeAlias = str
SemanticList: TypeAlias = List[Semantic]
Semantics: TypeAlias = SemanticList | Semantic

class _Comparable(object):

  """Rich comparison operators based on __lt__ and __eq__."""

  __gt__ = lambda self, other: not self < other and not self == other
  __le__ = lambda self, other: self < other or self == other
  __ne__ = lambda self, other: not self == other
  __ge__ = lambda self, other: self > other or self == other


class VersionError(Exception):
    pass


_re = re.compile('^'
                 '(\d+)\.(\d+)\.(\d+)'  # minor, major, patch
                 '(-[0-9A-Za-z-\.]+)?'  # pre-release
                 '(\+[0-9A-Za-z-\.]+)?'  # build
                 '$')


class _Seq(_Comparable):

  """Sequence of identifies that could be compared according to semver."""
  
  def __init__(self, seq):
    self.seq = seq
  
  def __lt__(self, other):
    assert set([int, str]) >= set(map(type, self.seq))
    for s, o in izip_longest(self.seq, other.seq):
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
  

def _try_int(s):
  assert type(s) is str
  try:
    return int(s)
  except ValueError:
    return s


def _make_group(g):
  return [] if g is None else list(map(_try_int, g[1:].split('.')))



class Version(_Comparable):

  def __init__(self, version: Semantics):
    checked = self._check(version)
    self._all_versions: list[str] = []
    
    if isinstance(version, list):
      self._all_versions = [str(v) for v in version if _re.match(v)]
      ver = sorted([Version(v) for v in self._all_versions], reverse=True)[-1].version

    if self._check(version):
      self.major, self.minor, self.patch = map(int, checked.groups()[:3])
      self.pre_release = _make_group(checked.group(4))
      self.build = _make_group(checked.group(5))
  
  def _check(self, version: Semantics):
    if isinstance(version, list):
      for v in version:
        match = _re.match(v)
        if not match:
          raise VersionError('invalid version %r' % v)
      return _re.match(version[-1])
    else:
      match = _re.match(version)
      if not match:
        raise VersionError('invalid version %r' % version)
      return match

  def add(self, version: Semantic):
    if version not in self._all_versions and self._check(version):
      self._all_versions.append(version)
  
  @property
  def latest(self) -> Version:
    sorted: list[str] = sorted(self._all_versions, reverse=True)
    return Version(sorted[0])
        
  @property
  def version(self) -> Semantic:
    return self.__str__()

  @property
  def versions(self) -> list[Version]:
    return [Version(v) for v in self._all_versions]
  
  def __str__(self):
    s = '.'.join(str(s) for s in self._mmp())
    if self.pre_release:
        s += '-%s' % '.'.join(str(s) for s in self.pre_release)
    if self.build:
        s += '+%s' % '.'.join(str(s) for s in self.build)
    return s
  
  def __repr__(self):
    return '%s(%r)' % (self.__class__.__name__, self.__str__())
  
  def _mmp(self):
    return [self.major, self.minor, self.patch]
  
  def __lt__(self, other):
    self._assume_to_be_comparable(other)
    if self._mmp() == other._mmp():
      if self.pre_release == other.pre_release:
        if self.build == other.build:
          return False
        elif self.build and other.build:
          return _Seq(self.build) < _Seq(other.build)
        elif self.build or other.build:
          return bool(other.build)
        assert not 'reachable'
      elif self.pre_release and other.pre_release:
        return _Seq(self.pre_release) < _Seq(other.pre_release)
      elif self.pre_release or other.pre_release:
        return bool(self.pre_release)
      assert not 'reachable'
    return self._mmp() < other._mmp()
  
  def __eq__(self, other):
    self._assume_to_be_comparable(other)
    return all([self._mmp() == other._mmp(),
                self.build == other.build,
                self.pre_release == other.pre_release])
  
  def _assume_to_be_comparable(self, other):
    if not isinstance(other, Version):
      raise TypeError('cannot compare `%r` with `%r`' % (self, other))
  