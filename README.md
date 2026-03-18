# Version
### Python Semantic Versioning

A lightweight Python library for parsing, comparing, and managing [Semantic Version](https://semver.org/) strings that gives you a single, well-tested `Version` class that handles the full SemVer specification correctly — including the subtleties of pre-release and build metadata ordering — with no external dependencies.
___ 


### Installation

Install **python-versioning** using pip:

```shell
pip install python-versioning
```
**Requirements:** Python 3.7+
___


## Features
- **Single Class** &mdash; A single `Version` class that handles semantic versioning.
- **Full SemVer Support** &mdash; Supports Major, minor, patch, pre-release and build metadata
- **Comparable** &mdash; All six comparison operators are built in (`<`, `<=`, `>`, `>=`, `==`, `!=`)
- **Track Multiple Versions** &mdash; Track mulitple versions in a single instance.

---

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

### Track Multiple Versions

Initialize with a list and the object is automatically set to the latest valid version:

```python
v = Version(['1.0.0', '3.2.1', '2.0.0-beta', 'not-a-version'])
print(v)  # '3.2.1'  — invalid entries are silently skipped
```

Add additional versions over time. If a new version is added, it becomes latest version:

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
v.remove('1.0.0') # Cannot remove this version
```

Removing the latest version reverts to the next latest:

```python
v = Version('1.0.0')
v.add('2.0.0')
v.add('2.1.0')
print(v.version)      # '2.1.0'

v.remove('2.1.0') 
print(v.version)      # '2.0.0'
```

### Get the latest tracked version

```python
v = Version('1.0.0')
v.add('3.0.0')
v.add('2.0.0')
print(v.latest)  # '3.0.0'
```

### Inspect all tracked versions

```python
v = Version(['1.0.0', '2.0.0', '3.0.0'])
for version in v.versions:
    print(version)
# 1.0.0
# 2.0.0
# 3.0.0
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
| `versions` | `list[Version]` | All tracked versions as `Version` objects |
| `latest` | `Version` | Highest version in the tracked list |

### `Version.add(version: str) -> None`

Adds a version string to the tracked list. No-op if already present. Raises `VersionError` if the string is invalid.

### `Version.remove(version: str) -> None`

Removes a version string from the tracked list. Raises `VersionError` if attempt to remove only version.

### `VersionError`

Subclass of `Exception`. Raised when a version string does not conform to the SemVer format.

---

## Run Tests

**80/80 tests passed**

```bash
python -m pytest tests/test.py -v
```
