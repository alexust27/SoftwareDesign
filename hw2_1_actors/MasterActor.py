from datetime import timedelta

from thespian.actors import Actor, ActorExitRequest, WakeupMessage

from ChildActor import ChildActor
from SearchUtils import SearchRequest, SEARCHERS


class MasterActor(Actor):
    def __init__(self):
        super().__init__()
        self.time_for_wait = timedelta(milliseconds=200)
        self.result = {}
        self.__search_systems = list(SEARCHERS)
        self.__counter = 0
        self.__main_sender = 0

    def receiveMessage(self, msg, sender):
        if isinstance(msg, timedelta):
            self.time_for_wait = msg
        elif isinstance(msg, str):
            self.handleDeadLetters(startHandling=False)
            self.__main_sender = sender
            for searcher in SEARCHERS:
                child_actor = self.createActor(ChildActor, globalName=searcher)
                self.send(child_actor, SearchRequest(searcher, msg))
            self.wakeupAfter(self.time_for_wait)

        elif isinstance(msg, WakeupMessage):
            self.__search_systems.reverse()
            for i in range(self.__counter):
                self.__search_systems.pop()
            for searcher in self.__search_systems:
                self.result.update({searcher: []})

            self.send(self.__main_sender, self.result)
            self.send(self.myAddress, ActorExitRequest())

        elif isinstance(msg, dict):

            self.result.update(msg)

            self.__counter += 1
            if len(self.__search_systems) == self.__counter:
                self.send(self.__main_sender, self.result)
                self.send(self.myAddress, ActorExitRequest())
