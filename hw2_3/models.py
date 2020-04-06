import datetime

TIME_FORMAT = "%m/%d/%Y"


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
        for e in events:
            if e.get_event_type() == ENTER:
                saved_e = e
            if e.get_event_type() == EXIT:
                self.add_visit(e.get_time() - saved_e.get_time())

    def add_visit(self, duration):
        self.visits += 1
        self.common_duration += duration

    def calc_visits(self):
        return self.common_duration / self.visits
