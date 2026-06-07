import unittest

from src import Version, VersionError, MAJOR, MINOR, PATCH, BUILD

class TestVersionParsing(unittest.TestCase):
    """Tests for parsing valid and invalid version strings."""

    def test_basic_version(self):
        v = Version('1.2.3')
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)

    def test_zero_version(self):
        v = Version('0.0.0')
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 0)

    def test_large_numbers(self):
        v = Version('100.200.300')
        self.assertEqual(v.major, 100)
        self.assertEqual(v.minor, 200)
        self.assertEqual(v.patch, 300)

    def test_pre_release(self):
        v = Version('1.0.0-alpha')
        self.assertEqual(v.pre_release, ['alpha'])

    def test_pre_release_with_dot(self):
        v = Version('1.0.0-alpha.1')
        self.assertEqual(v.pre_release, ['alpha', 1])

    def test_pre_release_numeric(self):
        v = Version('1.0.0-1')
        self.assertEqual(v.pre_release, [1])

    def test_pre_release_complex(self):
        v = Version('1.0.0-alpha.beta.1')
        self.assertEqual(v.pre_release, ['alpha', 'beta', 1])

    def test_build_metadata(self):
        v = Version('1.0.0+build.1')
        self.assertEqual(v.build, ['build', 1])

    def test_pre_release_and_build(self):
        v = Version('1.0.0-alpha+001')
        self.assertEqual(v.pre_release, ['alpha'])
        self.assertEqual(v.build, [1])

    def test_no_pre_release(self):
        v = Version('1.0.0')
        self.assertEqual(v.pre_release, [])

    def test_no_build(self):
        v = Version('1.0.0')
        self.assertEqual(v.build, [])

    def test_invalid_missing_patch(self):
        with self.assertRaises(VersionError):
            Version('1.0')

    def test_invalid_missing_minor_patch(self):
        with self.assertRaises(VersionError):
            Version('1')

    def test_invalid_letters_in_core(self):
        with self.assertRaises(VersionError):
            Version('a.b.c')

    def test_invalid_empty_string(self):
        with self.assertRaises(VersionError):
            Version('')

    def test_invalid_leading_v(self):
        with self.assertRaises(VersionError):
            Version('v1.0.0')

    def test_invalid_extra_segments(self):
        with self.assertRaises(VersionError):
            Version('1.0.0.0')

    def test_invalid_negative(self):
        with self.assertRaises(VersionError):
            Version('-1.0.0')

    def test_invalid_spaces(self):
        with self.assertRaises(VersionError):
            Version('1.0.0 ')


class TestVersionStringRepresentation(unittest.TestCase):
    """Tests for __str__ and __repr__."""

    def test_str_basic(self):
        self.assertEqual(str(Version('1.2.3')), '1.2.3')

    def test_str_with_pre_release(self):
        self.assertEqual(str(Version('1.0.0-alpha.1')), '1.0.0-alpha.1')

    def test_str_with_build(self):
        self.assertEqual(str(Version('1.0.0+build.1')), '1.0.0+build.1')

    def test_str_with_pre_release_and_build(self):
        self.assertEqual(str(Version('1.0.0-beta+exp.sha.5114f85')), '1.0.0-beta+exp.sha.5114f85')

    def test_repr(self):
        self.assertEqual(repr(Version('1.2.3')), "Version('1.2.3')")

    def test_version_property(self):
        v = Version('2.0.0')
        self.assertEqual(v.version, '2.0.0')


class TestVersionComparison(unittest.TestCase):
    """Tests for comparison operators."""

    def test_equal(self):
        self.assertEqual(Version('1.0.0'), Version('1.0.0'))

    def test_not_equal_patch(self):
        self.assertNotEqual(Version('1.0.0'), Version('1.0.1'))

    def test_not_equal_minor(self):
        self.assertNotEqual(Version('1.0.0'), Version('1.1.0'))

    def test_not_equal_major(self):
        self.assertNotEqual(Version('1.0.0'), Version('2.0.0'))

    def test_lt_patch(self):
        self.assertLess(Version('1.0.0'), Version('1.0.1'))

    def test_lt_minor(self):
        self.assertLess(Version('1.0.0'), Version('1.1.0'))

    def test_lt_major(self):
        self.assertLess(Version('1.0.0'), Version('2.0.0'))

    def test_gt_patch(self):
        self.assertGreater(Version('1.0.1'), Version('1.0.0'))

    def test_gt_minor(self):
        self.assertGreater(Version('1.1.0'), Version('1.0.0'))

    def test_gt_major(self):
        self.assertGreater(Version('2.0.0'), Version('1.0.0'))

    def test_le_less(self):
        self.assertLessEqual(Version('1.0.0'), Version('1.0.1'))

    def test_le_equal(self):
        self.assertLessEqual(Version('1.0.0'), Version('1.0.0'))

    def test_ge_greater(self):
        self.assertGreaterEqual(Version('1.0.1'), Version('1.0.0'))

    def test_ge_equal(self):
        self.assertGreaterEqual(Version('1.0.0'), Version('1.0.0'))

    def test_compare_with_non_version_raises(self):
        with self.assertRaises(TypeError):
            Version('1.0.0') < '1.0.1'

    def test_compare_with_non_version_eq_raises(self):
        with self.assertRaises(TypeError):
            Version('1.0.0') == '1.0.0'


class TestVersionPreReleaseComparison(unittest.TestCase):
    """Tests for pre-release comparison rules per SemVer spec."""

    def test_pre_release_less_than_release(self):
        self.assertLess(Version('1.0.0-alpha'), Version('1.0.0'))

    def test_release_greater_than_pre_release(self):
        self.assertGreater(Version('1.0.0'), Version('1.0.0-alpha'))

    def test_alpha_less_than_beta(self):
        self.assertLess(Version('1.0.0-alpha'), Version('1.0.0-beta'))

    def test_numeric_pre_release_less_than_alpha(self):
        self.assertLess(Version('1.0.0-1'), Version('1.0.0-alpha'))

    def test_pre_release_numeric_ordering(self):
        self.assertLess(Version('1.0.0-1'), Version('1.0.0-2'))

    def test_pre_release_dot_extends(self):
        self.assertLess(Version('1.0.0-alpha'), Version('1.0.0-alpha.1'))

    def test_pre_release_alpha_1_less_than_alpha_beta(self):
        self.assertLess(Version('1.0.0-alpha.1'), Version('1.0.0-alpha.beta'))

    def test_pre_release_equal(self):
        self.assertEqual(Version('1.0.0-alpha.1'), Version('1.0.0-alpha.1'))

    def test_semver_spec_precedence_order(self):
        versions = [
            '1.0.0-alpha',
            '1.0.0-alpha.1',
            '1.0.0-alpha.beta',
            '1.0.0-beta',
            '1.0.0-beta.2',
            '1.0.0-beta.11',
            '1.0.0-rc.1',
            '1.0.0',
        ]
        parsed = [Version(v) for v in versions]
        self.assertEqual(parsed, sorted(parsed))


class TestVersionBuildComparison(unittest.TestCase):
    """Tests for build metadata comparison."""

    def test_build_less_than_no_build(self):
        self.assertLess(Version('1.0.0+build'), Version('1.0.0'))

    def test_build_ordering(self):
        self.assertLess(Version('1.0.0+1'), Version('1.0.0+2'))

    def test_build_equal(self):
        self.assertEqual(Version('1.0.0+build.1'), Version('1.0.0+build.1'))

    def test_build_not_equal(self):
        self.assertNotEqual(Version('1.0.0+build.1'), Version('1.0.0+build.2'))


class TestVersionListInitialization(unittest.TestCase):
    """Tests for initializing Version with a list."""

    def test_list_picks_latest(self):
        v = Version(['1.0.0', '2.0.0', '1.5.0'])
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 0)

    def test_list_single_item(self):
        v = Version(['3.1.4'])
        self.assertEqual(v.major, 3)
        self.assertEqual(v.minor, 1)
        self.assertEqual(v.patch, 4)

    def test_list_skips_invalid(self):
        v = Version(['1.0.0', 'bad', '2.0.0'])
        self.assertEqual(v.major, 2)

    def test_list_all_invalid_raises(self):
        with self.assertRaises(VersionError):
            Version(['bad', 'also-bad', 'nope'])

    def test_empty_list_raises(self):
        with self.assertRaises(VersionError):
            Version([])

    def test_list_stores_valid_versions(self):
        v = Version(['1.0.0', '2.0.0', 'invalid'])
        self.assertEqual(len(v._all_versions), 2)


class TestVersionAddMethod(unittest.TestCase):
    """Tests for the add() method."""

    def test_add_new_version(self):
        v = Version('1.0.0')
        v.add('2.0.0')
        self.assertIn('2.0.0', v._all_versions)

    def test_add_duplicate_ignored(self):
        v = Version('1.0.0')
        v.add('1.0.0')
        self.assertEqual(v._all_versions.count('1.0.0'), 1)

    def test_add_invalid_raises(self):
        v = Version('1.0.0')
        with self.assertRaises(VersionError):
            v.add('not-a-version')

    def test_add_multiple(self):
        v = Version('1.0.0')
        v.add('2.0.0')
        v.add('3.0.0')
        self.assertEqual(len(v._all_versions), 3)


class TestVersionLatestProperty(unittest.TestCase):
    """Tests for the latest property."""

    def test_latest_from_list(self):
        v = Version(['1.0.0', '3.0.0', '2.0.0'])
        self.assertEqual(v.latest, '3.0.0')

    def test_latest_after_add(self):
        v = Version('1.0.0')
        v.add('5.0.0')
        v.add('3.0.0')
        self.assertEqual(v.latest, '5.0.0')

    def test_latest_single_version(self):
        v = Version('1.2.3')
        self.assertEqual(v.latest, '1.2.3')

    def test_latest_returns_string(self):
        v = Version(['1.0.0', '2.0.0'])
        self.assertIsInstance(v.latest, str)


class TestVersionsProperty(unittest.TestCase):
    """Tests for the versions property."""

    def test_versions_from_list(self):
        v = Version(['1.0.0', '2.0.0', '3.0.0'])
        self.assertEqual(len(v.versions), 3)

    def test_versions_are_version_instances(self):
        v = Version(['1.0.0', '2.0.0'])
        for item in v.versions:
            self.assertIsInstance(item, Version)

    def test_versions_single(self):
        v = Version('1.0.0')
        self.assertEqual(len(v.versions), 1)
        self.assertEqual(v.versions[0], Version('1.0.0'))

    def test_versions_after_add(self):
        v = Version('1.0.0')
        v.add('2.0.0')
        self.assertEqual(len(v.versions), 2)


class TestVersionRemoveMethod(unittest.TestCase):
    """Tests for the remove() method."""

    def test_remove_non_current_version(self):
        v = Version(['1.0.0', '2.0.0', '3.0.0'])
        v.remove('1.0.0')
        self.assertNotIn('1.0.0', v._all_versions)

    def test_remove_current_version_updates_current(self):
        v = Version(['1.0.0', '2.0.0', '3.0.0'])
        v.remove('3.0.0')
        self.assertEqual(str(v), '2.0.0')

    def test_remove_current_version_picks_next_latest(self):
        v = Version(['1.0.0', '2.0.0', '3.0.0'])
        v.remove('3.0.0')
        self.assertEqual(v.latest, '2.0.0')

    def test_remove_middle_version(self):
        v = Version(['1.0.0', '2.0.0', '3.0.0'])
        v.remove('2.0.0')
        self.assertNotIn('2.0.0', v._all_versions)
        self.assertEqual(str(v), '3.0.0')

    def test_remove_reduces_tracked_count(self):
        v = Version(['1.0.0', '2.0.0', '3.0.0'])
        v.remove('1.0.0')
        self.assertEqual(len(v._all_versions), 2)

    def test_remove_nonexistent_raises(self):
        v = Version(['1.0.0', '2.0.0'])
        with self.assertRaises(VersionError):
            v.remove('9.9.9')

    def test_remove_only_version_raises(self):
        v = Version('1.0.0')
        with self.assertRaises(VersionError):
            v.remove('1.0.0')

    def test_remove_leaves_remaining_intact(self):
        v = Version(['1.0.0', '2.0.0', '3.0.0'])
        v.remove('2.0.0')
        remaining = [str(ver) for ver in v.versions]
        self.assertIn('1.0.0', remaining)
        self.assertIn('3.0.0', remaining)


class TestVersionIncrementMethod(unittest.TestCase):
    """Tests for the increment() method."""

    def test_increment_patch(self):
        v = Version('1.2.3')
        v.increment(PATCH)
        self.assertEqual(str(v), '1.2.4')

    def test_increment_minor(self):
        v = Version('1.2.3')
        v.increment(MINOR)
        self.assertEqual(str(v), '1.3.0')

    def test_increment_major(self):
        v = Version('1.2.3')
        v.increment(MAJOR)
        self.assertEqual(str(v), '2.0.0')

    def test_increment_minor_resets_patch(self):
        v = Version('1.2.9')
        v.increment(MINOR)
        self.assertEqual(str(v), '1.3.0')

    def test_increment_major_resets_minor_and_patch(self):
        v = Version('1.9.9')
        v.increment(MAJOR)
        self.assertEqual(str(v), '2.0.0')

    def test_increment_adds_to_tracked_list(self):
        v = Version('1.0.0')
        v.increment(PATCH)
        self.assertIn('1.0.1', v._all_versions)

    def test_increment_tracked_count_increases(self):
        v = Version('1.0.0')
        v.increment(PATCH)
        self.assertEqual(len(v._all_versions), 2)

    def test_increment_updates_latest(self):
        v = Version('1.0.0')
        v.increment(MINOR)
        self.assertEqual(v.latest, '1.1.0')

    def test_increment_clears_pre_release(self):
        v = Version('1.0.0-alpha')
        v.increment(PATCH)
        self.assertEqual(str(v), '1.0.1')
        self.assertEqual(v.pre_release, [])

    def test_increment_clears_build(self):
        v = Version('1.0.0+build.1')
        v.increment(PATCH)
        self.assertEqual(str(v), '1.0.1')
        self.assertEqual(v.build, [])

    def test_increment_build_no_existing_defaults_to_b1(self):
        v = Version('1.0.0')
        v.increment(BUILD)
        self.assertEqual(str(v), '1.0.0+b1')

    def test_increment_build_b_prefix(self):
        v = Version('1.0.0+b1')
        v.increment(BUILD)
        self.assertEqual(str(v), '1.0.0+b2')

    def test_increment_build_numeric_last_element(self):
        v = Version('1.0.0+build.3')
        v.increment(BUILD)
        self.assertEqual(str(v), '1.0.0+build.4')

    def test_increment_build_pure_integer(self):
        v = Version('1.0.0+5')
        v.increment(BUILD)
        self.assertEqual(str(v), '1.0.0+6')

    def test_increment_build_no_trailing_digits_appends(self):
        v = Version('1.0.0+nightly')
        v.increment(BUILD)
        self.assertEqual(str(v), '1.0.0+nightly.1')

    def test_increment_build_preserves_pre_release(self):
        v = Version('1.0.0-alpha')
        v.increment(BUILD)
        self.assertEqual(str(v), '1.0.0-alpha+b1')

    def test_increment_build_adds_to_tracked_list(self):
        v = Version('1.0.0')
        v.increment(BUILD)
        self.assertIn('1.0.0+b1', v._all_versions)

    def test_increment_build_multiple_times(self):
        v = Version('1.0.0')
        v.increment(BUILD)
        v.increment(BUILD)
        self.assertEqual(str(v), '1.0.0+b2')

    def test_increment_invalid_part_raises(self):
        v = Version('1.0.0')
        with self.assertRaises(ValueError):
            v.increment('invalid')

    def test_increment_multiple_times(self):
        v = Version('1.0.0')
        v.increment(PATCH)
        v.increment(PATCH)
        self.assertEqual(str(v), '1.0.2')
        self.assertEqual(len(v._all_versions), 3)


if __name__ == '__main__':
    unittest.main()
