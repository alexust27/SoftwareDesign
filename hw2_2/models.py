from enum import Enum


class Currency(Enum):
    RUB = 1.
    EURO = 80.
    USD = 70.


def str_to_currency(s: str) -> Currency:
    if s == Currency.RUB.name:
        return Currency.RUB
    elif s == Currency.EURO.name:
        return Currency.EURO
    elif s == Currency.USD.name:
        return Currency.USD
    raise ValueError(s + " isn't a valid Currency")


class User:
    def __init__(self, u_id: int = None, login="", currency=Currency.RUB):
        self._id = u_id
        self._login = login
        self._currency = currency

    def to_dict(self):
        return {'u_id': self._id,
                'login': self._login,
                'currency': self._currency.name
                }

    def get_id(self):
        return self._id

    def get_currency(self):
        return self._currency

    def __str__(self):
        return str({
            "user_id": self._id,
            "login": self._login,
            "currency": self._currency.name
        })


class Product:
    def init_by_dict(self, d: dict):
        self._id = d["p_id"]
        self._name = d["name"]
        self._price = d["price"]

    def __init__(self, p_id: int = None, name="", price: float = 0, currency=Currency.RUB):
        self._id = p_id
        self._name = name
        assert Currency.RUB.value == 1.
        self._price = price * currency.value  # храним стоимость товара в рублях
        self._currency = currency

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def to_dict(self):
        return {
            "p_id": self._id,
            "name": self._name,
            "price": self._price
        }

    def to_str(self, currency=None):
        currency = self._currency if currency is None else currency
        return str({
            "product_id": self._id,
            "name": self._name,
            "price": str(self._price / currency.value) + " " + currency.name
        })
