# -*- coding: utf-8 -*-
# ==============================================================================

import os
import re
from datetime import date, timedelta
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import FormRequest, Request
from webscraperapp.models import SampleModel


class spidersample(CrawlSpider):
    """
    Spider detail
    """
    name = 'spidername'
    allowed_domains = ['<your-domain>.com']
    login_url = '<url>'
    username = os.getenv('user') or 'user'
    password = os.getenv('pass') or 'pass'
    start_urls = [
        '<url-one>',
        '<url-two>'
    ]
    page_xpath = ('//a[@rel="next"]',) 
    item_xpath = ('//a[contains(@class, "card--link")]',)
    rules = (
        Rule(
            LxmlLinkExtractor(
                restrict_xpaths=next_page_xpath,
            ),
            follow=True,
        ),
        Rule(
            LxmlLinkExtractor(restrict_xpaths=item_xpath),
            process_links='process_links_handler',
            callback='parse_item'
        )
    )

    def start_requests(self):
        yield Request(
            self.login_url,
            callback=self.parse_login)

    def parse_login(self, response):
        return FormRequest.from_response(
            response,
            formdata={
                'user[email]': self.username,
                'user[password]': self.password
            },
            callback=self.parse_login_response)

    def parse_login_response(self, response):
        error_message = "<text-here>"
        flash_message = response.xpath(
            '<xpath-here>')

        if error_message in flash_message.extract():
            raise Exception(
                'Login error, Please check the email and password.')
        else:
            return super(spidersample, self).start_requests()

    def process_links_handler(self, links):
        filtered_links = filter(
            lambda link:
            # Logic here
            ,
            links)

        return filtered_links

    def extract_date_from_text(self, texts):
        try:
           # Logic here
        except AttributeError:
            pass

        return None

    def extract_data_from_link(self, url):
        # logic here

    def get_xpath_details(self, response, label):
        selector = response.xpath("<xpath-here>")
        return selector

    def item_details(self):
        item = {
            # item fields here
        }
        return item_html

    def extract_details_from_list(self, item):
        # Concatenate list of strings
        # Logic here
        return item

    def parse_item_detail(self, response):
        # Logic here
        return self.extract_details_from_list(item_list)
