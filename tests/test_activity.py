import sys
import tempfile
import unittest
from datetime import date,timedelta
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import activity

TODAY=date(2026,10,4)
def fixture():
    parts=[]
    for i in range(365):
        day=TODAY-timedelta(days=364-i)
        count=0 if i%3 else 2
        level=0 if count==0 else 1
        parts.append(f'<td id="day-{i}" data-date="{day}" data-level="{level}"></td>')
        parts.append(f'<tool-tip for="day-{i}">{"No" if count==0 else count} contributions on October 4th.</tool-tip>')
    return ''.join(parts)

class CalendarTests(unittest.TestCase):
    def test_zero_and_active_days_totals(self):
        days=activity.parse_calendar(fixture(),TODAY)
        self.assertEqual(len(days),365)
        self.assertEqual(sum(x['count'] for x in days),244)
        self.assertEqual(sum(x['count']>0 for x in days),122)
        self.assertEqual(days[0]['date'],'2025-10-05')

    def test_missing_tooltip_rejected(self):
        with self.assertRaisesRegex(ValueError,'tooltip'):
            activity.parse_calendar(fixture().replace('for="day-0"','for="other"'),TODAY)

    def test_future_dates_not_included(self):
        future=TODAY+timedelta(days=1)
        html=fixture()+f'<td id="future" data-date="{future}" data-level="4"></td><tool-tip for="future">99 contributions on October 5th.</tool-tip>'
        days=activity.parse_calendar(html,TODAY)
        self.assertEqual(len(days),365)
        self.assertEqual(sum(x['count'] for x in days),244)

    def test_stale_calendar_and_mismatched_counts_rejected(self):
        with self.assertRaisesRegex(ValueError,'stale'):
            activity.parse_calendar(fixture(),TODAY+timedelta(days=30))
        with self.assertRaisesRegex(ValueError,'disagree'):
            activity.parse_calendar(fixture().replace('data-level="1"','data-level="0"',1),TODAY)

    def test_bad_level_and_non_calendar_rejected(self):
        for html in ('<html>Unavailable</html>',fixture().replace('data-level="1"','data-level="9"',1)):
            with self.assertRaises(ValueError): activity.parse_calendar(html,TODAY)

    def test_duplicate_and_gap_rejected(self):
        first=(TODAY-timedelta(days=364)).isoformat()
        second=(TODAY-timedelta(days=363)).isoformat()
        with self.assertRaises(ValueError):
            activity.parse_calendar(fixture().replace(second,first),TODAY)
        with self.assertRaises(ValueError):
            activity.parse_calendar(fixture().replace(first,'2025-10-03'),TODAY)

    def test_failure_preserves_all_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            for name in activity.OUTPUTS: (Path(folder)/name).write_bytes(b'previous good output')
            def offline(_): raise OSError('network unavailable')
            for fetcher in (offline,lambda _: '<html>Broken</html>'):
                with self.assertRaises((OSError,ValueError)):
                    activity.update('suren1013',folder,fetcher=fetcher,today=TODAY)
                for name in activity.OUTPUTS:
                    self.assertEqual((Path(folder)/name).read_bytes(),b'previous good output')

    def test_valid_update_and_repeat_are_deterministic(self):
        with tempfile.TemporaryDirectory() as folder:
            data=activity.update('suren1013',folder,fetcher=lambda _:fixture(),today=TODAY)
            self.assertEqual(data['total'],244)
            first={name:(Path(folder)/name).read_bytes() for name in activity.OUTPUTS}
            activity.update('suren1013',folder,fetcher=lambda _:fixture(),today=TODAY)
            self.assertEqual(first,{name:(Path(folder)/name).read_bytes() for name in activity.OUTPUTS})
            self.assertTrue(first['activity-landscape.png'].startswith(b'\x89PNG'))

if __name__=='__main__': unittest.main()
