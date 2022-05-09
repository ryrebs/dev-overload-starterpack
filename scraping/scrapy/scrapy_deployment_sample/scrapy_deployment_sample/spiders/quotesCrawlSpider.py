# -*- coding: utf-8 -*-

# Using a generic spider
# Extract and follow external links as long as it follow the Rule specified


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request
from scrapy.http import FormRequest

class QuotesSpider(CrawlSpider):
    name = 'quotesCs'
    allowed_domains = ['toscrape.com', 'goodreads.com']
    login_url = ['http://quotes.toscrape.com/login']
    start_urls = ['http://quotes.toscrape.com','http://goodreads.com']
    rules = [
        Rule(LxmlLinkExtractor(allow=(r'/author/show/\d+\.[\w_]+')), callback='parse_goodreads_author'),
        # for every response extract this pattern
        # if this link is extracted, should we follow again and proceed with parsing the next response? True
        Rule(LxmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="next"]')), follow=True), 
        # for every response extract this link pattern
        # match only pattern on this domain, used if multiple start urls
        # process_links are the links extracted from the  page
        # process request for every page, must return request or None
        Rule(LxmlLinkExtractor(allow=(r'/author/[\w\.]+'), allow_domains=['toscrape.com']), process_links='handler', process_request='handler', callback='parse_quotes_author')
    ]


    # Override the start_requests method
    # to start with the login_url
    def start_request(self, response):
        yield Request(
            url=self.login_url,
            callback=self.login)


    def login(self, response):
        payload = {
            'username': 'scraper',
            'password': 'password'
        }
        yield FormRequest.from_response(
            response,
            formdata=payload,
            callback=super().start_requests(response) 
            # Call the original start_request
            # to start processing start_urls 
        )

    # change login to accomodate each caller
    def handler(self, value):
        try:
            self.logger.info('***** -->> %s' % value)
        except TypeError:
            pass

    def parse_goodreads_author(self, response):
        author_name = response.xpath('//h1[@class="authorName"]/span/text()').extract_first()        
        yield {
            'author_name_goodreads': author_name
        } 

    def parse_quotes_author(self, response):
        author_name = response.xpath('//h3[@class="author-title"]/text()').extract_first().strip()        
        yield {
            'author_name': author_name
        } 