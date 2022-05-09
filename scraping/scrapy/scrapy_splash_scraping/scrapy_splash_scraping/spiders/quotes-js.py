# scraping content generated with javascript
# actual elements are not included in the page source
# make sure you have scrapy-splash instance running
# docker instance 
#    $ docker pull scrapinghub/splash
#    $ docker run -p 8050:8050 scrapinghub/splash


import scrapy
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = 'quotesjs'
    

    def start_requests(self):
        yield SplashRequest(
            url='http://quotes.toscrape.com/js',
            callback=self.parse
        )

    def parse(self, response):
        # self.logger.info('Crawling this website: ' + response.url)
        
        # Using css selectors
        # extract all quotes from the page
        # but yield each data individually
        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tag': quote.css('a.tag::text').extract()
            }   
            yield item
