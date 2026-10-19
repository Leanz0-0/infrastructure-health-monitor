
import unittest
from src.alert_rules import is_sustained_high


class TestSustainedHigh(unittest.TestCase):

    def test_temporary_spike(self):
        self.assertFalse(is_sustained_high([95, 20, 18]))

    def test_sustained_high_usage(self):
        self.assertTrue(is_sustained_high([91, 93, 89]))

    def test_insufficient_samples(self):
        self.assertFalse(is_sustained_high([96, 97]))

    def test_recovery_before_alert(self):
        self.assertFalse(is_sustained_high([92, 94, 72]))

    def test_threshold_boundary(self):
        self.assertTrue(is_sustained_high([85, 85, 85]))

    def test_only_latest_samples(self):
        self.assertTrue(is_sustained_high([20, 91, 92, 93]))


if __name__ == "__main__":
    unittest.main()
