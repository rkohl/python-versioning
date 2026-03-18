import sys
import os
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime, timedelta
from src import *

# TEST FOR
# CleanPath
# Duration
# Evaluated
# ExtEnum
# ExtStrEnum
# ExtIntEnum
# File
# mergeListByKey
# NotGiven
# NotGivenOr
# NOTGIVEN
# OrdinalNumber
# numberOrdinal
# Percentage
# precision
# prettyPrint
# Progress
# Ratio
# Serialization
# splitList
# taskDuration
# TimeRemaining
# TimeSince
# UntilTime
# JSON
# Data
# ModeledData
# RawJSON
# between
# betweenInclusive

class TestUtility(unittest.TestCase):

  def test_cleanPath(self):
    self.assertEqual(CleanPath.clean("/users/<int:id>"), "/users/id")

  def test_duration(self):
    start = datetime(2025, 1, 1, 0, 0, 0)
    end = datetime(2025, 1, 1, 1, 0, 0)
    duration = Duration(start, end)
    self.assertEqual(duration.seconds, 3600)
    self.assertEqual(duration.formatted, "1hr")

  def test_ordinalNumber(self):
    self.assertEqual(OrdinalNumber(1).ordinal, "1st")
    self.assertEqual(OrdinalNumber(2).ordinal, "2nd")
    self.assertEqual(OrdinalNumber(3).ordinal, "3rd")
    self.assertEqual(OrdinalNumber(4).ordinal, "4th")
    self.assertEqual(OrdinalNumber(11).ordinal, "11th")
    self.assertEqual(OrdinalNumber(12).ordinal, "12th")
    self.assertEqual(OrdinalNumber(13).ordinal, "13th")
    self.assertEqual(OrdinalNumber(21).ordinal, "21st")
    self.assertEqual(OrdinalNumber(22).ordinal, "22nd")
    self.assertEqual(OrdinalNumber(23).ordinal, "23rd")
    self.assertEqual(OrdinalNumber(24).ordinal, "24th")
    self.assertEqual(OrdinalNumber(101).ordinal, "101st")
    self.assertEqual(OrdinalNumber(102).ordinal, "102nd")
    self.assertEqual(OrdinalNumber(103).ordinal, "103rd")
    self.assertEqual(OrdinalNumber(104).ordinal, "104th")
    self.assertEqual(OrdinalNumber(111).ordinal, "111th")
    self.assertEqual(OrdinalNumber(112).ordinal, "112th")
    self.assertEqual(OrdinalNumber(113).ordinal, "113th")

  def test_percentage(self):
    self.assertEqual(Percentage(0.5).decimal, 0.5)
    self.assertEqual(Percentage(0.5).percent, "50.0%")
    self.assertEqual(Percentage(0.5).fraction, "50/100")

  def test_precision(self):
    self.assertEqual(precision(1), 0)
    self.assertEqual(precision(0.5), 1)
    self.assertEqual(precision(0.05), 2)
    self.assertEqual(precision(0.005), 3)
    self.assertEqual(precision(0.0005), 4)
    self.assertEqual(precision(0.004232340051111901), 18)

  def test_ratio(self):
    self.assertEqual(Ratio(1, 2).ratio, "1:2")
    self.assertEqual(Ratio(1, 2).value, 0.5)

  def test_progress(self):
    self.assertEqual(Progress(0.4, 1).percent, 40.0)
    self.assertEqual(Progress(1, 2).value, 0.5)
    self.assertEqual(Progress(1, 2).percent, 50.0)

  def test_between(self):
    self.assertTrue(between(5, 1, 10))
    self.assertFalse(between(5, 1, 5))
    self.assertFalse(between(5, 5, 10))
    self.assertFalse(between(5, 1, 5))
    self.assertFalse(between(5, 5, 10))
    self.assertTrue(betweenInclusive(5, 1, 10))
    self.assertTrue(betweenInclusive(5, 1, 5))
    self.assertTrue(betweenInclusive(5, 5, 10))

  def test_mergeListByKey(self):
    list1 = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
    list2 = [{"id": 1, "age": 30}, {"id": 3, "name": "Bob"}]
    self.assertEqual(mergeListByKey(list1, list2, "id"), [{"id": 1, "name": "John", "age": 30}, {"id": 2, "name": "Jane"}, {"id": 3, "name": "Bob"}])

  def test_splitList(self):
    self.assertEqual(splitList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11]])

  def test_file(self):
    file = File("test.txt")
    self.assertEqual(file.ext, ".txt")
    self.assertEqual(file.name, "test.txt")
    self.assertEqual(file.filename, "test.txt")

class TestEnums(unittest.TestCase):
  """Test cases for the ExtEnum, ExtStrEnum, and ExtIntEnum classes."""

  def test_ext_enum(self):
    """Test ExtEnum functionality."""
    class TestEnum(ExtEnum):
        VALUE1 = 1
        VALUE2 = 2
        VALUE3 = 3

    self.assertEqual(TestEnum.names(), ['VALUE1', 'VALUE2', 'VALUE3'])
    self.assertEqual(TestEnum.values(), [1, 2, 3])
    self.assertEqual(TestEnum.commaSeperatedValues(), '1,2,3')
    self.assertEqual(TestEnum.keyValueDict(), {'VALUE1': 1, 'VALUE2': 2, 'VALUE3': 3})
    self.assertEqual(len(TestEnum.cases()), 3)
    self.assertIsInstance(TestEnum.VALUE1, TestEnum)

  def test_ext_str_enum(self):
    """Test ExtStrEnum functionality."""
    class TestStrEnum(ExtStrEnum):
        VALUE1 = "value1"
        VALUE2 = "value2"

    self.assertEqual(TestStrEnum.names(), ['VALUE1', 'VALUE2'])
    self.assertEqual(TestStrEnum.values(), ['value1', 'value2'])
    self.assertEqual(TestStrEnum.commaSeperatedValues(), 'value1,value2')
    self.assertEqual(TestStrEnum.keyValueDict(), {'VALUE1': 'value1', 'VALUE2': 'value2'})
    self.assertEqual(len(TestStrEnum.cases()), 2)
    self.assertIsInstance(TestStrEnum.VALUE1, TestStrEnum)

  def test_ext_int_enum(self):
    """Test ExtIntEnum functionality."""
    class TestIntEnum(ExtIntEnum):
        VALUE1 = 1
        VALUE2 = 2

    self.assertEqual(TestIntEnum.names(), ['VALUE1', 'VALUE2'])
    self.assertEqual(TestIntEnum.values(), [1, 2])
    self.assertEqual(TestIntEnum.commaSeperatedValues(), '1,2')
    self.assertEqual(TestIntEnum.keyValueDict(), {'VALUE1': 1, 'VALUE2': 2})
    self.assertEqual(len(TestIntEnum.cases()), 2)
    self.assertEqual(1, TestIntEnum.VALUE1)
    self.assertIsInstance(TestIntEnum.VALUE1, TestIntEnum)
    
class TestDuration(unittest.TestCase):
  """Test cases for the Duration class."""

  def test_duration_initialization_valid(self):
      """Test valid duration initialization."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 1, 0, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.start, start)
      self.assertEqual(duration.end, end)

  def test_duration_initialization_invalid(self):
      """Test that ValueError is raised when start > end."""
      start = datetime(2025, 1, 1, 1, 0, 0)
      end = datetime(2025, 1, 1, 0, 0, 0)
      with self.assertRaises(ValueError):
          Duration(start, end)

  def test_duration_same_times(self):
      """Test duration when start and end are the same."""
      time = datetime(2025, 1, 1, 0, 0, 0)
      duration = Duration(time, time)
      self.assertEqual(duration.seconds, 0)
      self.assertEqual(duration.formatted, "0s")

  def test_seconds_property_30_seconds(self):
      """Test seconds property calculation for 30 seconds."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 0, 0, 30)
      duration = Duration(start, end)
      self.assertEqual(duration.seconds, 30)

  def test_seconds_property_1_hour(self):
      """Test seconds property calculation for 1 hour."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 1, 0, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.seconds, 3600)

  def test_seconds_property_1_day(self):
      """Test seconds property calculation for 1 day."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 2, 0, 0, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.seconds, 86400)

  def test_formatted_30_seconds(self):
      """Test formatted output for 30 seconds."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 0, 0, 30)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "30s")

  def test_formatted_45_seconds(self):
      """Test formatted output for 45 seconds."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 0, 0, 45)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "45s")

  def test_formatted_1_minute(self):
      """Test formatted output for 1 minute."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 0, 1, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "1m")

  def test_formatted_90_seconds(self):
      """Test formatted output for 1.5 minutes."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 0, 1, 30)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "1.5m")

  def test_formatted_1_hour(self):
      """Test formatted output for 1 hour."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 1, 0, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "1hr")

  def test_formatted_1_5_hours(self):
      """Test formatted output for 1.5 hours."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 1, 1, 30, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "1.5hr")

  def test_formatted_1_day(self):
      """Test formatted output for 1 day."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 2, 0, 0, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "1d")

  def test_formatted_7_days(self):
      """Test formatted output for 7 days."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 8, 0, 0, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "7d")

  def test_formatted_multiple_days_with_decimal(self):
      """Test formatted output for 2.5 days."""
      start = datetime(2025, 1, 1, 0, 0, 0)
      end = datetime(2025, 1, 3, 12, 0, 0)
      duration = Duration(start, end)
      self.assertEqual(duration.formatted, "2.5d")

class TestTimeRemaining(unittest.TestCase):
  """Test cases for the TimeRemaining class."""

  def test_time_remaining_initialization(self):
      """Test TimeRemaining initialization with a future datetime."""
      future = datetime.now() + timedelta(hours=1)
      tr = TimeRemaining(future)
      self.assertIsNotNone(tr.formatted)
      self.assertTrue(len(tr.formatted) > 0)

  def test_time_remaining_hours_and_minutes(self):
      """Test TimeRemaining with 1 hour and 20 minutes."""
      future = datetime.now() + timedelta(hours=1, minutes=20)
      tr = TimeRemaining(future)
      self.assertIn("hr", tr.formatted)
      self.assertIn("min", tr.formatted)

  def test_time_remaining_days(self):
      """Test TimeRemaining with multiple days."""
      future = datetime.now() + timedelta(days=5)
      tr = TimeRemaining(future)
      self.assertIn("d", tr.formatted)

  def test_time_remaining_weeks_and_days(self):
      """Test TimeRemaining with weeks and days."""
      future = datetime.now() + timedelta(weeks=1, days=3)
      tr = TimeRemaining(future)
      self.assertIn("wk", tr.formatted)
      self.assertIn("d", tr.formatted)

  def test_time_remaining_months_and_days(self):
      """Test TimeRemaining with months and days."""
      future = datetime.now() + timedelta(days=90)
      tr = TimeRemaining(future)
      # Should contain months or days
      self.assertTrue("m" in tr.formatted or "d" in tr.formatted)

  def test_time_remaining_years_months_days(self):
      """Test TimeRemaining with years, months, and days."""
      future = datetime.now() + timedelta(days=365 + 90 + 2)
      tr = TimeRemaining(future)
      self.assertIn("yr", tr.formatted)

  def test_time_remaining_seconds_only(self):
      """Test TimeRemaining with just seconds."""
      future = datetime.now() + timedelta(seconds=30)
      tr = TimeRemaining(future)
      self.assertIn("s", tr.formatted)

  def test_time_remaining_minutes_only(self):
      """Test TimeRemaining with just minutes."""
      future = datetime.now() + timedelta(minutes=5)
      tr = TimeRemaining(future)
      self.assertIn("min", tr.formatted)

  def test_time_remaining_hours_only(self):
      """Test TimeRemaining with just hours."""
      future = datetime.now() + timedelta(hours=3)
      tr = TimeRemaining(future)
      self.assertIn("hr", tr.formatted)

  def test_time_remaining_multiple_units(self):
      """Test TimeRemaining with multiple combined units."""
      future = datetime.now() + timedelta(days=2, hours=5, minutes=30)
      tr = TimeRemaining(future)
      parts = tr.formatted.split()
      # Should have at least 2 parts when multiple units exist
      self.assertTrue(len(parts) >= 2)

  def test_time_remaining_all_units_zero(self):
      """Test TimeRemaining when time has already passed (returns 0s)."""
      past = datetime.now() - timedelta(seconds=1)
      tr = TimeRemaining(past)
      # Should still return a formatted string
      self.assertIsNotNone(tr.formatted)

  def test_time_remaining_zero_time(self):
      """Test TimeRemaining with zero remaining time."""
      now = datetime.now()
      tr = TimeRemaining(now)
      self.assertIsNotNone(tr.formatted)

  def test_time_remaining_properties_exist(self):
      """Test that all TimeRemaining properties are accessible."""
      future = datetime.now() + timedelta(days=1, hours=2, minutes=30)
      tr = TimeRemaining(future)
      self.assertIsNotNone(tr.seconds)
      self.assertIsNotNone(tr.minutes)
      self.assertIsNotNone(tr.hours)
      self.assertIsNotNone(tr.days)
      self.assertIsNotNone(tr.weeks)
      self.assertIsNotNone(tr.months)
      self.assertIsNotNone(tr.years)
      self.assertIsNotNone(tr.formatted)

  def test_time_remaining_properties_are_floats(self):
      """Test that time unit properties are floats."""
      future = datetime.now() + timedelta(hours=1)
      tr = TimeRemaining(future)
      self.assertIsInstance(tr.seconds, float)
      self.assertIsInstance(tr.minutes, float)
      self.assertIsInstance(tr.hours, float)
      self.assertIsInstance(tr.days, float)
      self.assertIsInstance(tr.weeks, float)
      self.assertIsInstance(tr.months, float)
      self.assertIsInstance(tr.years, float)

  def test_time_remaining_complex_duration(self):
      """Test TimeRemaining with a complex duration."""
      future = datetime.now() + timedelta(
          days=365 + 30 + 7 + 2,
          hours=5,
          minutes=45,
          seconds=30
      )
      tr = TimeRemaining(future)
      # Should contain multiple units
      self.assertTrue("yr" in tr.formatted or "m" in tr.formatted)
      # Formatted should not be empty
      self.assertTrue(len(tr.formatted) > 0)
    
if __name__ == '__main__':
  unittest.main()