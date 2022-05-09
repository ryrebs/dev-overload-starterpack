import scrapy
import json

class QuoteScroll(scrapy.Spider):
    name = 'QuoteScroll'
    api_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [api_url.format(1)]


    # parsing an infinite scroll data on a webpage
    # by accessing directly an api
    # check first if has an api
    # and check the keys and values on scrapy shell
    def parse(self, response):
        data = json.loads(response.text)
        for quote in data['quotes']:
            yield {
                'author-name': quote['author']['name'],
                'text': quote['text'],
                'tags': quote['tags']
            }

        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(url=self.api_url.format(next_page), callback=self.parse)