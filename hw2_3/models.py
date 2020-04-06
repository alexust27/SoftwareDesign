import datetime
from collections import defaultdict

TIME_FORMAT = "%d/%m/%Y %H:%M"
DATE_FORMAT = "%d/%m/%Y"


class Pass:
    def __init__(self, pass_id: int = None,
                 start_time: datetime.datetime = None,
                 finish_time: datetime.datetime = None):
        self.pass_id = pass_id
        self.start_time = start_time
        self.finish_time = finish_time

    def get_id(self):
        return self.pass_id

    def get_finish_time(self):
        return self.finish_time

    def __str__(self):
        return str({
            "pass_id": self.pass_id,
            "start_time": self.start_time.strftime(TIME_FORMAT),
            "finish_time": self.finish_time.strftime(TIME_FORMAT)
        })


ENTER = 0
EXIT = 1


class Event:

    def __init__(self, pass_id: int = None, event_type=None, time: datetime.datetime = None):
        self.pass_id = pass_id
        self.event_type = event_type
        self.time = time

    def get_event_type(self):
        return self.event_type

    def get_time(self):
        return self.time

    def get_id(self):
        return self.pass_id

    def __str__(self):
        return str({
            "pass_id": self.pass_id,
            "event": "exit" if self.event_type == EXIT else "enter",
            "time": self.time.strftime(TIME_FORMAT)
        })


class Statistic:
    def __init__(self, events=[]):
        self.common_duration = datetime.timedelta(0)
        self.visits = 0
        saved_e = None
        self.report_by_day = defaultdict(list)
        for e in events:
            self.add_event(e)
            if e.get_event_type() == ENTER:
                saved_e = e
            if e.get_event_type() == EXIT:
                self.add_visit(e.get_time() - saved_e.get_time())

    def add_visit(self, duration):
        self.visits += 1
        self.common_duration += duration

    def calc_visits_in_minutes(self):
        return self.common_duration.total_seconds() / self.visits / 60

    def add_event(self, e):
        self.report_by_day[e.get_time().strftime(DATE_FORMAT)].append(e)

    def get_report_by_days(self) -> str:
        res = ""
        for date, events in self.report_by_day.items():
            res += date + " : [\n"
            for e in events:
                res += str(e) + ",\n"
            res = res[:-2]
            res += "\n ],\n"
        res = res[:-2]
        return res
