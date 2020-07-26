from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from typing import Generator
from data.articles import Article

import requests
from requests.exceptions import HTTPError, Timeout


class Website(ABC):
    def __init__(self, name, search_url):
        self.name = name
        self.search_url = search_url

    @abstractmethod
    def get_url(self, search_terms:str) -> str:
        pass

    def get_soup(self, search_terms: str) -> BeautifulSoup:
        """ Search 'search_terms' in the website and give me a BeautifulSoup object as a response """

        url = self.get_url(search_terms)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except Timeout:
            raise
        except HTTPError:
            raise

        source = response.content

        return BeautifulSoup(source, 'lxml')

    # TODO: Implement a failback
    def dump_source(self, path: str):
        pass

    @abstractmethod
    def get_articles(self, search_terms: str) -> Generator[Article, None, None]:
        """ Generator function that outputs Article objects out of the search terms """
        pass
