from .website import Website
from data.articles import Article

from bs4 import BeautifulSoup
from datetime import datetime
from typing import Generator


class Mercadolibre(Website):
    def __init__(self):
        super().__init__(name='MERCADOLIBRE', search_url='https://listado.mercadolibre.cl/')
        self.currency = 'CLP'

    def get_url(self, search_terms: str) -> str:
        """ Whatever the string is; format it as foo-bar.html and concatenate it to the website url """

        split = search_terms.split()
        url = self.search_url + '-'.join(split)

        return url

    # TODO: Implement shipping cost
    @staticmethod
    def get_shipping_cost(article_url):
        pass

    @staticmethod
    def parse_article(unparsed_article: BeautifulSoup) -> dict:
        """ Helper function to parse the content wrapper """

        span_title = unparsed_article.find('a', class_='ui-search-item__group__element ui-search-link')
        price = ( unparsed_article.find('span', class_='price-tag-fraction') ).get_text()

        return {
            'price': {'real_price': price},
            'url': span_title.get('href'),
            'title': span_title.get('title'),
        }

    def get_articles(self, search_terms: str) -> Generator[Article, None, None]:
        soup = self.get_soup(search_terms)
        unparsed_articles = soup.find_all('div', class_='ui-search-result__content-wrapper')

        for unparsed_article in unparsed_articles:
            parsed = self.parse_article(unparsed_article)

            yield Article(
                origin=self.name,
                currency=self.currency,
                date_scraped=datetime.now(),
                **parsed
            )
