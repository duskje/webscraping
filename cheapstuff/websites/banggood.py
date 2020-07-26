from .website import Website
from data.articles import Article

from bs4 import BeautifulSoup
from datetime import datetime
from typing import Generator


class Banggood(Website):
    def __init__(self):
        super().__init__(name='BANGGOOD', search_url='https://usa.banggood.com/search/')
        self.currency = 'USD'

    def get_url(self, search_terms: str) -> str:
        """ Whatever the string is; format it as foo-bar.html and concatenate it to the website url """

        split = search_terms.split()
        url = self.search_url + '-'.join(split) + '.html'

        return url

    # TODO: Implement shipping cost
    @staticmethod
    def get_shipping_cost(article_url):
        pass

    @staticmethod
    def parse_article(unparsed_article: BeautifulSoup) -> dict:
        """ Straight up parsing """

        span_title = unparsed_article.find('span', class_='title')
        prices = unparsed_article.find('span', class_='price wh_cn')

        price = {
            'max_price': prices.get('oriattrmax'),
            'min_price': prices.get('oriattrmin')
        }

        return {
            'price': price,
            'url': span_title.find('a').get('href'),
            'title': span_title.find('a').get('title'),
        }

    def get_articles(self, search_terms: str) -> Generator[Article, None, None]:
        soup = self.get_soup(search_terms)
        unparsed_articles = soup.find_all('li', class_='shopslist')

        for unparsed_article in unparsed_articles:
            parsed = self.parse_article(unparsed_article)

            yield Article(
                origin=self.name,
                currency=self.currency,
                date_scraped=datetime.now(),
                **parsed
            )


