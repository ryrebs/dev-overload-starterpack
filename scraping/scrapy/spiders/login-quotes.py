import scrapy


class LoginQuotes(scrapy.Spider):
    name = 'loginquotes'
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]


    # entry point
    # first request and response
    def parse(self, response):
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        payload = {
            'csrf_token': token,
            'username': 'anyuser', # input with name='username'
            'password': 'anypassword' # input with name='password'
        }
        # simulate post request
        yield scrapy.FormRequest(url=self.login_url, 
                                formdata=payload, 
                                callback=self.parse_quotes)


    def parse_quotes(self, response):
        # parse the main page, choose data to parse
        # check if the goodreads url have shown
        # else log in have failed
        
        for q in response.css('div.quote'):
            yield {
                'author-name' : q.css('small.author::text').extract_first(),
                'author-url': q.css('small.author ~ a[href*="goodreads.com"]::attr(href)').extract_first()
            }