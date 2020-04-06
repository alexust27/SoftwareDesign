from pymongo import MongoClient
from mongo import passes_repository, events_repository


class MongoFitnessContext:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.get_database("fitness")

        self.events = events_repository.EventsRepository(db)
        self.passes = passes_repository.PassRepository(db)


class StatusCode:
    OK = 200
    NOT_IN_DATABASE = 201
    OLD_PASS = 202
    ALREADY_IN = 203
    NOT_ENTER = 204
    CANT_CREATE = 205
