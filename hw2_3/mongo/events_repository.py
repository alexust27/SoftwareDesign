import pymongo

from models import Event
from mongo import mongo_repository_base


class EventsRepository(mongo_repository_base.FitnessDB):
    class Meta:
        model = Event
        collection_name = "events"

    def get_all_events(self):
        events = self.c().find({}).sort([("time", pymongo.ASCENDING)])
        converted = []
        for e in events:
            converted.append(self.convert_to_model(e))
        return converted

    def get_last_event_by_id(self, pass_id):
        result = self.c().find({"pass_id": pass_id}).sort([("time", pymongo.DESCENDING)])
        for e in result:
            converted = self.convert_to_model(e)
            return converted
        else:
            return None
