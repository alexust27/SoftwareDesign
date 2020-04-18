import tornado.ioloop
import tornado.web
import tornado.locks
import tornado.httpserver

from context import MotorDB
from models import Product, Currency, User, str_to_currency


class UserHandler(tornado.web.RequestHandler):
    async def post(self):
        u_id = int(self.get_argument("id", None))
        login = self.get_argument("login", None)
        currency = self.get_argument("currency", None)
        currency = Currency.RUB if currency is None else str_to_currency(currency)

        user = User(u_id, login, currency)
        await self.application.db.insert(user)
        self.write(user.__str__() + " was saved")


class ProductsHandler(tornado.web.RequestHandler):
    async def post(self):
        prod_id = int(self.get_argument("id", None))
        prod_name = self.get_argument("name", None)
        prod_price = float(self.get_argument("price", None))
        currency = self.get_argument("currency", None)
        currency = Currency.RUB if currency is None else str_to_currency(currency)

        p = Product(prod_id, prod_name, prod_price, currency=currency)
        await self.application.db.insert(p, False)
        self.write(p.to_str() + " was saved")

    async def get(self):
        user_id = int(self.get_argument("u_id", None))
        cur = await self.application.db.get_cur_for_user(user_id)
        products = await self.application.db.get_products()
        res = '"products": [\n'
        for p in products:
            res += p.to_str(currency=cur) + '\n'
        res += "]"
        self.write(res)


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write("Hello, world")


class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
            (r"/", MainHandler),
            (r"/user", UserHandler),
            (r"/products", ProductsHandler),
        ]
        settings = dict(
            title="Catalog",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    context = MotorDB()
    app = Application(context)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8005)
    server.start(1)

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
