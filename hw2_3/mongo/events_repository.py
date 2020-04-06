import pymongo

from models import Event
from mongo import mongo_repository_base


class EventsRepository(mongo_repository_base.FitnessDB):
    class Meta:
        model = Event
        collection_name = "events"

    def get_all_evensts(self):
        events = self.c().find().sort([("time", pymongo.ASCENDING)])
        if events.cursor_id is None:
            return []
        converted = [self.convert_to_model(e) for e in events]
        return converted

    def get_event_by_id(self, pass_id):
        result = self.c().find_one({"pass_id": pass_id})
        if result is None:
            return None

        converted = self.convert_to_model(result)
        return converted
