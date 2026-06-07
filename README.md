# Version
## Python Semantic Versioning

- **Single Class** &mdash; A single `Version` class that handles semantic versioning.
- **Full SemVer Support** &mdash; Supports major, minor, patch, pre-release and build metadata
- **Comparable** &mdash; All six comparison operators are built in (`<`, `<=`, `>`, `>=`, `==`, `!=`)
- **Track Multiple Versions** &mdash; Track multiple versions in a single instance.
- **Increment** &mdash; Bump major, minor, patch, or build with a single call.

`Version` is a lightweight Python library for working with [Semantic Version (SemVer)](https://semver.org/). It provides a single `Version` class that handles the full lifecycle of version strings — parsing, validating, comparing, and managing collections of them.

At its core, the library solves a common pain point: version strings look simple but have non-obvious ordering rules, especially once pre-release tags and build metadata are involved. Rather than reaching for a heavyweight dependency or writing fragile string comparisons, you get a focused tool that implements the SemVer 2.0.0 spec correctly and completely.

A `Version` can be created from a single string or a list of strings. When given a list, it automatically filters out anything malformed and sets itself to the highest valid entry. From there you can add, remove, and increment versions in the tracked set, inspect the full list, or ask for the latest at any time — with the current version always kept in sync as the tracked set changes.

Comparisons use all six standard operators and follow the spec's precedence rules precisely: numeric identifiers sort as integers, alphanumeric identifiers sort lexically, numeric identifiers rank below alphanumeric ones, a shorter pre-release ranks below a longer one with the same prefix, and any pre-release at all ranks below the equivalent release version.

---

### Installation

Install **python-versioning** using pip:

```shell
pip install python-versioning
```
**Requirements:** Python 3.7+
___


## Usage

First import:

```python
from version import Version
```

### Major, Minor, Patch

Define `Version` class with SemVer `1.4.2`:

```python
from version import Version

v = Version('1.4.2')
print(v.major)        # 1
print(v.minor)        # 4
print(v.patch)        # 2
print(v.version)      # '1.4.2'
```

### Pre-release and build metadata

Define `Version` class with SemVer `2.0.0-alpha.1+build.42`:

```python
from version import Version

v = Version('2.0.0-alpha.1+build.42')
print(v.major)        # 2
print(v.minor)        # 0
print(v.patch)        # 0
print(v.pre_release)  # ['alpha', 1]
print(v.build)        # ['build', 42]
print(v.version)      # '2.0.0-alpha.1+build.42'
```

### Compare versions

All six comparison operators are supported (`<`, `<=`, `>`, `>=`, `==`, `!=`):

```python
Version('1.0.0') < Version('2.0.0')       # True
Version('1.0.0-alpha') < Version('1.0.0') # True  (pre-release < release)
Version('1.0.0') == Version('1.0.0')      # True
Version('2.0.0') > Version('1.9.9')       # True
```
Comparing against a non-`Version` raises a `TypeError`:

```python
Version('1.0.0') < '1.0.1'  # raises TypeError
```

### Increment a version

Use the `MAJOR`, `MINOR`, `PATCH`, and `BUILD` constants with `increment()` to bump a version. The incremented version is added to the tracked list and becomes the current version.

```python
from version import Version, MAJOR, MINOR, PATCH, BUILD

v = Version('1.2.3')

v.increment(PATCH)   # 1.2.4  — patch bumped
v.increment(MINOR)   # 1.3.0  — minor bumped, patch reset
v.increment(MAJOR)   # 2.0.0  — major bumped, minor and patch reset
```

Incrementing `BUILD` defaults to `+b1` if no build metadata is set, otherwise it increments the trailing number:

```python
v = Version('1.0.0')
v.increment(BUILD)   # 1.0.0+b1

v.increment(BUILD)   # 1.0.0+b2

v = Version('1.0.0+build.4')
v.increment(BUILD)   # 1.0.0+build.5
```

Pre-release is preserved when incrementing build:

```python
v = Version('1.0.0-alpha')
v.increment(BUILD)   # 1.0.0-alpha+b1
```

Incrementing `MAJOR`, `MINOR`, or `PATCH` clears any pre-release and build metadata per the SemVer spec.

### Track Multiple Versions

Initialize with a list and the object is automatically set to the latest valid version:

```python
v = Version(['1.0.0', '3.2.1', '2.0.0-beta', 'not-a-version'])
print(v)  # '3.2.1'  — invalid entries are silently skipped
```

Add additional versions over time. If a new version is added that is higher than the current, it becomes the latest:

```python
v = Version('1.0.0')
print(v.version)      # '1.0.0'

v.add('2.0.0')
print(v.version)      # '2.0.0'

v.add('1.5.0')
print(v.version)      # '2.0.0'

v.add('3.0.1')
print(v.version)      # '3.0.1'
```

Duplicates are ignored and invalid strings raise `VersionError`:

```python
v.add('1.0.0')        # no-op, already tracked
v.add('bad-version')  # raises VersionError
```

Remove versions:

```python
v = Version('1.0.0')
v.add('2.0.0')
v.remove('1.0.0')
```

Removing the only version raises `VersionError`:

```python
v = Version('1.0.0')
v.remove('1.0.0')  # raises VersionError: Cannot remove this version
```

Removing the current version reverts to the next latest:

```python
v = Version('1.0.0')
v.add('2.0.0')
v.add('2.1.0')
print(v.version)      # '2.1.0'

v.remove('2.1.0')
print(v.version)      # '2.0.0'
```

### Get the latest tracked version

`latest` returns the highest version string in the tracked list:

```python
v = Version('1.0.0')
v.add('3.0.0')
v.add('2.0.0')
print(v.latest)       # '3.0.0'
print(type(v.latest)) # <class 'str'>
```

### Inspect all tracked versions

`versions` returns all tracked versions as `Version` objects, sorted highest first:

```python
v = Version(['1.0.0', '2.0.0', '3.0.0'])
for version in v.versions:
    print(version)
# 3.0.0
# 2.0.0
# 1.0.0
```

---

## Comparison Rules

This library follows the [SemVer 2.0.0 specification](https://semver.org/) exactly:

1. **Major, minor, patch** are compared numerically.
2. **Pre-release** versions have *lower* precedence than the release version (`1.0.0-alpha < 1.0.0`).
3. When both versions have a pre-release, identifiers are compared left to right:
   - Numeric identifiers are compared as integers.
   - Alphanumeric identifiers are compared lexically.
   - Numeric identifiers always have *lower* precedence than alphanumeric ones (`1 < alpha`).
   - A shorter pre-release has lower precedence than a longer one with the same prefix (`alpha < alpha.1`).
4. **Build metadata** follows the same ordering rules as pre-release, and a version with build metadata has lower precedence than one without.

The full canonical precedence order from the SemVer spec:

```
1.0.0-alpha
1.0.0-alpha.1
1.0.0-alpha.beta
1.0.0-beta
1.0.0-beta.2
1.0.0-beta.11
1.0.0-rc.1
1.0.0
```

---

## Error Handling

`VersionError` is raised for any invalid version string:

```python
Version('')           # VersionError: invalid version ''
Version('v1.0.0')     # VersionError: invalid version 'v1.0.0'
Version('1.0')        # VersionError: invalid version '1.0'
Version([])           # VersionError: No versions provided in the list
Version(['bad'])      # VersionError: No valid versions found in the list
```

---

# API Reference

```python
Version(version: str | list[str])
```

Creates a `Version` instance.

- If given a **string**, parses and validates it.
- If given a **list**, filters out invalid entries, raises if none remain, and sets the instance to the highest valid version.

| Attribute / Property | Type | Description |
|---|---|---|
| `major` | `int` | Major version number |
| `minor` | `int` | Minor version number |
| `patch` | `int` | Patch version number |
| `pre_release` | `list[int \| str]` | Parsed pre-release identifiers |
| `build` | `list[int \| str]` | Parsed build metadata identifiers |
| `version` | `str` | String form of this version |
| `versions` | `list[Version]` | All tracked versions as `Version` objects, sorted highest first |
| `latest` | `str` | Highest version string in the tracked list |

### `Version.add(version: str) -> None`

Adds a version string to the tracked list. No-op if already present. Raises `VersionError` if the string is invalid. Updates the current version if the new one is higher.

### `Version.remove(version: str) -> None`

Removes a version string from the tracked list. Raises `VersionError` if the version is not tracked or if it is the only version remaining. If the removed version was the current version, the next highest becomes current.

### `Version.increment(part: str) -> None`

Bumps the specified part of the version using one of the exported constants:

| Constant | Effect |
|---|---|
| `MAJOR` | Increments major, resets minor and patch to `0`, clears pre-release and build |
| `MINOR` | Increments minor, resets patch to `0`, clears pre-release and build |
| `PATCH` | Increments patch, clears pre-release and build |
| `BUILD` | Increments build metadata; defaults to `+b1` if none is set |

The new version is appended to the tracked list and becomes the current version. Raises `ValueError` for an unrecognised part.

### `VersionError`

Subclass of `Exception`. Raised when a version string does not conform to the SemVer format, or when a tracked-list operation cannot be completed (e.g. removing the last version).

---

## Run Tests

**100/100 tests passed**

```bash
python -m pytest tests/test.py -v
```
