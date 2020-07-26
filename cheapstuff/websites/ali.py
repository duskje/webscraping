from .website import Website
from data.articles import Article

from bs4 import BeautifulSoup
from datetime import datetime
from typing import Generator


class Aliexpress(Website):
    def __init__(self):
        super().__init__('ALIEXPRESS', 'https://www.aliexpress.com/af/')

    def get_url(self, search_terms: str) -> str:

        split = search_terms.split()
        url = self.search_url + '-'.join()

        return url
