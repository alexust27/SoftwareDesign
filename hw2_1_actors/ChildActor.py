from thespian.actors import Actor, ActorExitRequest

from SearchUtils import SearchRequest, DummySearchClient


class ChildActor(Actor):
    def __init__(self):
        super().__init__()
        self.__search_client = DummySearchClient()

    def receiveMessage(self, msg, sender):
        if isinstance(msg, SearchRequest):
            res = self.__search_client.search_for(msg)
            self.send(sender, res)

            self.send(self.myAddress, ActorExitRequest())
