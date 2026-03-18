import unittest
from datetime import datetime, timedelta
from xutil.datetime.duration import Duration
from xutil.datetime.remaining import TimeRemaining


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
