from unittest import TestCase

from envents_statistic import EventsStatisticImpl
from clock_for_test import SetableClock

SEC_IN_HOUR = 3600
SEC_IN_MINUTE = 60


class TestEventStatistic(TestCase):
    def setUp(self):
        self.test_clock = SetableClock(1, 1, 1)
        self.event_statistic = EventsStatisticImpl(self.test_clock)

    def test_empty_events(self):
        self.assertEqual(self.event_statistic.get_event_statistic_by_name('some event'), 0)

    def test_simple_inc(self):
        self.event_statistic.inc_event('event1')
        self.event_statistic.inc_event('event2')
        self.event_statistic.inc_event('event1')
        self.event_statistic.inc_event('event2')
        self.assertEqual(self.event_statistic.get_event_statistic_by_name('event1'), 2.0 / 60)
        self.assertEqual(self.event_statistic.get_event_statistic_by_name('event2'), 2.0 / 60)
        self.assertDictEqual(self.event_statistic.get_all_event_statistic(),
                             {'event1': 2.0 / 60, 'event2': 2.0 / 60})

    def test_old_events(self):
        self.event_statistic.inc_event('event1')
        self.event_statistic.inc_event('event1')
        self.test_clock.add_seconds(SEC_IN_HOUR + 1)
        self.assertEqual(self.event_statistic.get_event_statistic_by_name('event1'), 0)
        self.assertDictEqual(self.event_statistic.get_all_event_statistic(), {})

    def test_events_one_hour(self):
        for i in range(60):
            self.event_statistic.inc_event('event1')
            self.test_clock.add_seconds(SEC_IN_MINUTE)
        self.assertEqual(self.event_statistic.get_event_statistic_by_name('event1'), 1.0)

    def test_events(self):
        for i in range(6):
            self.event_statistic.inc_event('event1')
            self.test_clock.add_seconds(10 * SEC_IN_MINUTE)
        self.assertEqual(self.event_statistic.get_event_statistic_by_name('event1'), 1 / 10)
        for i in range(61):
            self.event_statistic.inc_event('event2')
            self.test_clock.add_seconds(SEC_IN_MINUTE)
        self.assertEqual(self.event_statistic.get_event_statistic_by_name('event2'), 1.0)

    def test_events2(self):
        for i in range(1, 4):
            self.event_statistic.inc_event('event1')
            self.event_statistic.inc_event('event2')
            self.test_clock.add_seconds(i * SEC_IN_MINUTE)
        self.assertDictEqual(self.event_statistic.get_all_event_statistic(),
                             {'event1': 1 / 20, 'event2': 1 / 20})
