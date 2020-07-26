from typing import Iterable
from datetime import datetime
from itertools import product

from mysql.connector import MySQLConnection
from mysql.connector.errors import ProgrammingError

class Article:
    def __init__(self, title: str, price: dict, url: str, date_scraped: datetime.now,
                 origin: str, shipping_cost=None, currency=None):
        self.title = title
        self.price = price
        self.url = url
        self.date_scraped = date_scraped
        self.from_website = origin
        self.shipping_cost = shipping_cost
        self.currency = currency

    def __eq__(self, obj):
        return self.url == obj.url

    @property
    def is_currency_set(self) -> bool:
        return self.currency is not None

    @property
    def total_cost(self) -> dict:
        # These both are in percentages
        VAT = 0.19
        RIPOFF_TAX = 0.06

        try:
            cif = {key: self.price[key] + self.shipping_cost for key in self.price}
        except ValueError as error:
            print('Warning: shipping_cost not set yet. Assuming zero though...', error, sep='\n')
            cif = self.price

        taxes_percentage = (1 + RIPOFF_TAX) * (1 + VAT)
        return {key: cif[key] * taxes_percentage for key in cif}

    def save_into_database(self, sql_cursor: MySQLConnection, values: Iterable, force: bool=False) -> None:
        object_dict = self.__dict__

        object_keys = set(object_dict.keys())

        matching_keys = frozenset( object_keys.intersection( set(values) ) )
        matching_object_dict = {key: object_dict[key] for key in matching_keys}

        # this looked like a very good idea two teas ago, guess not
        # TODO: Refactor this sql query
        sql_query = f"INSERT INTO articles ({ ', '.join(matching_keys) }) " \
                    f"VALUES({ ', '.join( ( '%(' + key + ')s'for key in matching_keys) ) })"

        try:
            sql_cursor.execute(sql_query, matching_object_dict)
        except ProgrammingError:
            raise
