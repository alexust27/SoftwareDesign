import datetime
from unittest import TestCase

from context import MongoFitnessContext
from models import DATE_FORMAT, Pass, Event, ENTER, TIME_FORMAT, EXIT


class TestMongo(TestCase):
    def setUp(self) -> None:
        self.context = MongoFitnessContext()

    def tearDown(self) -> None:
        self.context.events.drop()
        self.context.passes.drop()

    def test_get_pass(self):
        start_time = datetime.datetime.strptime("01/02/2019", DATE_FORMAT)
        finish_time = datetime.datetime.strptime("01/02/2020", DATE_FORMAT)
        pass_id = 1
        pass_old = Pass(pass_id, start_time, finish_time)
        self.context.passes.create(pass_old)
        res = self.context.passes.get_by_id(pass_id)

        self.assertEqual(res.get_id(), pass_id)
        self.assertEqual(res.get_finish_time(), finish_time)

    def test_update_pass(self):
        start_time = datetime.datetime.strptime("01/02/2019", DATE_FORMAT)
        time_old = datetime.datetime.strptime("01/02/2020", DATE_FORMAT)
        time_new = datetime.datetime.strptime("01/12/2020", DATE_FORMAT)
        pass_id = 0
        pass_old = Pass(pass_id, start_time, time_old)
        pass_new = Pass(pass_id, start_time, time_new)
        res = self.context.passes.create(pass_old)
        self.assertEqual(res.get_id(), pass_id)
        self.assertEqual(res.get_finish_time(), time_old)
        res = self.context.passes.update(pass_new)
        self.assertEqual(res.get_id(), pass_id)
        self.assertEqual(res.get_finish_time(), time_new)

    def test_get_event(self):
        pass_id = 0
        enter_time = datetime.datetime.strptime("01/02/2019 12:00", TIME_FORMAT)
        exit_time = datetime.datetime.strptime("01/02/2019 14:00", TIME_FORMAT)
        e = Event(pass_id, ENTER, enter_time)
        e2 = Event(pass_id, EXIT, exit_time)

        self.context.events.create(e)
        res = self.context.events.get_last_event_by_id(pass_id)

        self.assertEqual(res.get_id(), pass_id)
        self.assertEqual(res.get_time(), enter_time)
        self.assertEqual(res.get_event_type(), ENTER)

        self.context.events.create(e2)
        res = self.context.events.get_last_event_by_id(pass_id)

        self.assertEqual(res.get_id(), pass_id)
        self.assertEqual(res.get_time(), exit_time)
        self.assertEqual(res.get_event_type(), EXIT)

    def test_get_all_events(self):
        pass_id = 0
        enter_time = datetime.datetime.strptime("01/02/2019 12:00", TIME_FORMAT)
        exit_time = datetime.datetime.strptime("01/02/2019 14:00", TIME_FORMAT)
        e = Event(pass_id, ENTER, enter_time)
        e2 = Event(pass_id, EXIT, exit_time)

        res = self.context.events.get_all_events()
        self.assertEqual(0, len(res))

        self.context.events.create(e)
        self.context.events.create(e2)
        res = self.context.events.get_all_events()

        self.assertEqual(2, len(res))
        self.assertEqual(ENTER, res[0].get_event_type())
        self.assertEqual(EXIT, res[1].get_event_type())
