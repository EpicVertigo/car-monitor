from scrapy import Spider, Request
from carscraper.settings import GRAPH_QL_QUERY
from bs4 import BeautifulSoup as Soup


class AutoRiaSpider(Spider):
    name = 'autoria'
    start_urls = ['https://auto.ria.com/search/?categories.main.id=1&brand.id[0]=9&model.id[0]=3213&price.currency=1&abroad.not=0&custom.not=1&page=0&size=100&scrollToAuto=24809865']

    def __init__(self, query, *args, **kwargs):
        # self.start_urls = ['https://auto.ria.com/search/?{query}']
        super().__init__(*args, **kwargs)

    def parse(self, response):
        soup = Soup(response.body, 'lxml')
        import ipdb
        ipdb.set_trace()
        pass
