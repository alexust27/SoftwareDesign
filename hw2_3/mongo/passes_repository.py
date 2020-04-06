from models import Pass
from mongo import mongo_repository_base


class PassRepository(mongo_repository_base.FitnessDB):
    class Meta:
        model = Pass
        collection_name = "passes"

    def __init__(self, db):
        super(PassRepository, self).__init__(db)

    def get_by_id(self, pass_id):
        result = self.c().find_one({"pass_id": pass_id})
        if result is None:
            return None

        converted = self.convert_to_model(result)
        return converted

    def update(self, pass_: Pass):
        result = self.c().find_one_and_update({"pass_id": pass_.get_id()}, pass_.__dict__)
        if result is None:
            return None

        converted = self.convert_to_model(result)
        return converted
