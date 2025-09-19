import unittest
from datetime import datetime

from ...evaluator.time_features import DayOfWeek, DayOfMonth, MonthOfYear


class TestTimeFeatures(unittest.TestCase):

    def test_day_of_week_with_int(self):
        dow = DayOfWeek()
        # Should cycle: 1, 2, ..., 7, then repeat
        self.assertEqual(dow.evaluate(0), 1)
        self.assertEqual(dow.evaluate(1), 2)
        self.assertEqual(dow.evaluate(6), 7)
        self.assertEqual(dow.evaluate(7), 1)
        self.assertEqual(dow.evaluate(13), 7)
        self.assertEqual(dow.evaluate(14), 1)

    def test_day_of_week_with_datetime(self):
        dow = DayOfWeek()
        self.assertEqual(dow.evaluate(datetime(2024, 1, 1)), 1)  # Monday
        self.assertEqual(dow.evaluate(datetime(2024, 1, 7)), 7)  # Sunday
        self.assertEqual(dow.evaluate(datetime(2024, 1, 8)), 1)  # Next Monday

    def test_day_of_month_with_int(self):
        dom = DayOfMonth()
        self.assertEqual(dom.evaluate(0), 1)
        self.assertEqual(dom.evaluate(30), 31)
        self.assertEqual(dom.evaluate(31), 1)
        self.assertEqual(dom.evaluate(32), 2)

    def test_day_of_month_with_datetime(self):
        dom = DayOfMonth()
        self.assertEqual(dom.evaluate(datetime(2024, 1, 1)), 1)
        self.assertEqual(dom.evaluate(datetime(2024, 2, 28)), 28)
        self.assertEqual(dom.evaluate(datetime(2024, 2, 29)), 29)  # Leap year
        self.assertEqual(dom.evaluate(datetime(2024, 12, 31)), 31)

    def test_month_of_year_with_int(self):
        moy = MonthOfYear()
        self.assertEqual(moy.evaluate(0), 1)
        self.assertEqual(moy.evaluate(11), 12)
        self.assertEqual(moy.evaluate(12), 1)
        self.assertEqual(moy.evaluate(13), 2)

    def test_month_of_year_with_datetime(self):
        moy = MonthOfYear()
        self.assertEqual(moy.evaluate(datetime(2024, 1, 15)), 1)
        self.assertEqual(moy.evaluate(datetime(2024, 6, 1)), 6)
        self.assertEqual(moy.evaluate(datetime(2024, 12, 31)), 12)


if __name__ == "__main__":
    unittest.main()
