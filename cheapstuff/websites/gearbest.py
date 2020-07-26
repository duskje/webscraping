from .website import Website
from cheapstuff.data.articles import Article

from datetime import datetime

# TODO: doesn't work with BeautifulSoup

class Gearbest(Website):
    def __init__(self):
        super().__init__(name='GEARBEST', search_url='https://www.gearbest.com/sale/')

    def get_url(self, search_terms: str) -> str:
        """ Whatever the string is, format it as /foo-bar and concatenate it to the website url """

        split = search_terms.split()
        url = self.search_url + '-'.join(split)

        return url

    def parse_article(self, unparsed_article) -> dict:
        pass

    def get_articles(self, search_terms: str):
        pass
