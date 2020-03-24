import datetime

MINUTE_IN_HOUR = 60


class EventsStatistic:

    def inc_event(self, name):
        pass

    def get_event_statistic_by_name(self, name):
        pass

    def get_all_event_statistic(self):
        pass

    def print_statistic(self):
        pass


class EventsStatisticImpl(EventsStatistic):
    def __init__(self, clock: datetime.datetime):
        self.events = {}
        self.clock = clock

    def __remove_old(self, name):
        def check(t):
            if t < (self.clock.now() - datetime.timedelta(hours=1)).time():
                return False
            return True

        if not (name in self.events):
            return
        self.events[name] = list(filter(check, self.events[name]))
        if not self.events[name]:
            del self.events[name]

    @staticmethod
    def __count_rpm(times) -> float:
        return len(times) / MINUTE_IN_HOUR

    def inc_event(self, name: str) -> None:
        # self.__remove_old(name)
        if name in self.events.keys():
            self.events[name].append(self.clock.time())
        else:
            self.events[name] = [self.clock.time()]

    def get_event_statistic_by_name(self, name: str) -> float:
        self.__remove_old(name)
        if name in self.events:
            return self.__count_rpm(self.events[name])
        else:
            return 0

    def get_all_event_statistic(self) -> dict:
        statistic = {}
        keys = list(self.events.keys())
        for name in keys:
            self.__remove_old(name)
        for name in self.events.keys():
            statistic[name] = self.get_event_statistic_by_name(name)
        return statistic

    def print_statistic(self) -> None:
        statistic = self.get_all_event_statistic()
        for (event, rpm) in statistic.items():
            print('event="%s" with RPM=%f' % (event, rpm))
