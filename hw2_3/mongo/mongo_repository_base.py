class FitnessDB:
    def __init__(self, db):
        self.db = db

    def c(self):
        return getattr(self.db, self.Meta.collection_name)

    def create(self, item):
        data = item.__dict__
        self.c().insert_one(data)
        return item

    def convert_to_model(self, d):
        del d["_id"]
        x = self.Meta.model()
        x.__dict__.update(d)
        return x

    def drop(self):
        self.c().drop()
