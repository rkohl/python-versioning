# Changelog

All notable changes to this project are documented here.

---

## [1.1.0] — 2026-06-07

### Added

- **`Version.increment(part: str)`** — Bump a version component in place. The incremented version is appended to the tracked list and becomes the current version. Accepts one of four exported constants:

  | Constant | Behaviour |
  |---|---|
  | `MAJOR` | Increments major, resets minor and patch to `0`, clears pre-release and build |
  | `MINOR` | Increments minor, resets patch to `0`, clears pre-release and build |
  | `PATCH` | Increments patch, clears pre-release and build |
  | `BUILD` | Increments build metadata; defaults to `+b1` if none is set. Preserves pre-release. |

  Build increment rules:
  - No build set → `+b1`
  - Last identifier ends in digits (e.g. `b3`, `build.5`) → trailing number is incremented
  - Last identifier is a plain integer → incremented directly
  - Last identifier has no trailing digits → `.1` is appended


### Changed

- **`latest` property** now returns a `str` instead of a `Version` object, consistent with how version strings are handled throughout the API.

- **`versions` property** now returns all tracked versions sorted highest first (descending), making it easier to iterate from newest to oldest.

- **`add()` method** now updates the current version when the newly added version is higher than the current one.

### Internals

- Replaced the hand-rolled `_Comparable` mixin with `functools.total_ordering`, reducing boilerplate and delegating operator derivation to the standard library.
- Merged `_check` and `_set_version` into a single `_parse` method, removing a layer of indirection.
- Simplified `_Seq.__lt__` by removing runtime `assert` statements and tightening the loop logic.
- `__str__` uses an f-string for the `major.minor.patch` segment instead of joining a list.
- `__eq__` compares a single tuple on each side instead of three separate conditions.


---

## [1.0.0] — Initial release

- `Version` class with parsing, validation, and rich comparison for SemVer strings.
- Support for major, minor, patch, pre-release, and build metadata.
- List initialisation — automatically selects the highest valid version from a list.
- `add()` method for tracking additional versions over time.
- `remove()` method for removing tracked versions.
- `latest` and `versions` properties.
- `VersionError` exception for invalid version strings.
