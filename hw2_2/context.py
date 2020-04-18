import motor

from models import User, Product, str_to_currency, Currency


class MotorDB:
    def __init__(self):
        client = motor.motor_tornado.MotorClient('localhost', 27017)
        self._db = client['catalog_db']
        self.users = self._db.users
        self.products = self._db.products

    def get_db(self):
        return self._db

    async def insert(self, model, user=True):
        doc = dict(model.to_dict())
        print("inserting:", doc)
        collection = self.users if user else self.products
        await collection.insert_one(doc)

    async def get_cur_for_user(self, user_id):
        document = await self.users.find_one({'u_id': user_id})
        if document is None:
            return Currency.RUB
        return str_to_currency(document['currency'])

    async def get_products(self):
        res = []
        async for document in self.products.find():
            pr = Product()
            pr.init_by_dict(document)
            res.append(pr)
        return res
