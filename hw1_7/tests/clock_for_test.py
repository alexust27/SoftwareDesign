import datetime


class SetableClock(datetime.datetime):
    __now = datetime.datetime(2009, 1, 1, 1)

    def time(self) -> datetime.time:
        return self.__now.time()

    def now(self, **kwargs) -> datetime.datetime:
        return self.__now

    def set_time(self, time):
        self.__now = time
        return self

    def add_seconds(self, add):
        self.__now += datetime.timedelta(seconds=add)
        return self
