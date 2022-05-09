# -*- coding: utf-8 -*-
import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        
        # obtaining listing details
        # get the author details url
        author_urls = response.css('.author + a::attr(href)').extract()
        for url in author_urls:
            author_abs_url = response.urljoin(url)
            yield scrapy.Request(url=author_abs_url, callback=self.parse_details)



        # following pagination
        # joining next url with the base url
        next_page = response.css('li.next > a::attr(href)').extract_first()
        
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
    

    def parse_details(self, response):
        yield  {
            'author-name': response.css('.author-title::text').extract_first(),
            'birth_date': response.css('.author-description::text').extract_first()
        }