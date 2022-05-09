import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request

class QuoesSpiderTwo(CrawlSpider):
    name = 'quotesCs2'
    allowed_domain = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com',]

    rules = [
        Rule(LxmlLinkExtractor(
            # if empty match all 
            # this is default unless patterns are specified
            # allow(),
            # match only in this region
            restrict_xpaths=('//li[@class="next"]')), 
            # process links that were extracted using the pattern above,
            # allow() or restrict_xpaths()| or css selector (see documentation)
            process_links='next_links_handler',
            # make a request for each link extracted from the link extractor
            process_request='next_request_handler',
            # parse the response
            # from the request
            # the second response have already done
            # so this is the second page
            callback='parse_pages',
            # follow each response, and extract another links 
            follow=True),

        Rule(LxmlLinkExtractor(
            allow=(r'/author/[\w\.]+'),
            allow_domains=['toscrape.com']),
            # process all links extracted from this pattern
            # filtering purposes
            process_links='process_links_handler',
            # The requests for all the links 
            process_request='process_request_handler',
            # request is already dispatched
            # parse the response from the request, extracted from this link pattern
            callback='parse_quotes_author',)
            ]


    def parse_start_url(self, response):

        # The first rule cannot parse the first page
        # since the request has been already dispatched
        # for the next page
        # this is the response from the first request
        self.logger.info(response)    
        # create a request for this response
        # which is the first response from start_urls
        request = scrapy.Request(response.url,
                             callback=self.parse_pages)
        request.meta['item'] = 'from start url'
        return request

    def next_links_handler(self, links):
        self.logger.info("----->> Next links handler")
        self.logger.info(links)


        return links


    def parse_pages(self, response):
        try:
            self.logger.info(response.meta['item'])
        except KeyError:
            pass
            
        self.logger.info(' ----->> Parse_pages')
        self.logger.info(type(response))
        self.logger.info(response)

        text = response.xpath('//div[@class="quote"]/span[1]/text()').extract()

        self.logger.info(text)
        

        # should not return a response object
        return None

    def next_request_handler(self, request):
        self.logger.info(' ----->> Next_request_handler')
        self.logger.info(self)
        self.logger.info(request)
        self.logger.info(type(request)) # Request
        # return request to continue to next page if follow is true
        # this will serve  as the referer request
        return request

    def process_links_handler(self, links):
        self.logger.info('process_links_handler')
        self.logger.info(self)
        self.logger.info(links) # list of links, with each type of Link
        self.logger.info(type(links)) # List

        
        return links

    def process_request_handler(self, request):
        self.logger.info(' ----->> Process_request_handler')
        self.logger.info(self)
        self.logger.info(request)
        self.logger.info(type(request))
        return request

    def parse_quotes_author(self, response):
        self.logger.info('parse_quotes_author')
        self.logger.info(response)
        # self.logger.info(type(response))
        
        author_name = response.xpath('//h3[@class="author-title"]/text()').extract_first().strip()        
        yield {
            'author_name': author_name
        } 