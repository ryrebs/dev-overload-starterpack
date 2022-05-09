# -*- coding: utf-8 -*-
# ==============================================================================

import time
import pytest

from selenium import webdriver as wb
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from webscraperapp.spiders.<spider-here> import <spider-here>
from webscraperapp.pipelines import WebscraperappPipeline
from scrapy.http import HtmlResponse
from pyvirtualdisplay import Display
from <sampleitemtest> import detail
from scrapy.exceptions import DropItem


#*** Sample test setup for signing in ***# 

SIGN_URL = '<sign_in>'
USERNAME = <username> # from env
PASSWORD = <password> # from env
MAX_WAIT = 10


@pytest.fixture(scope="session")
def browser(request):
    display = Display(visible=0, size=(1024, 768))
    display.start()
    driver = wb.Chrome()

    def teardown():
        driver.quit()
        display.stop()
    request.addfinalizer(teardown)

    driver.get(SIGN_URL)
    driver.find_element_by_name('user[password]').send_keys(PASSWORD)
    driver.find_element_by_name('user[email]').send_keys(USERNAME)
    driver.find_element_by_xpath(
        '//button[@type="submit"]').send_keys(Keys.ENTER)

    return driver


@pytest.fixture(scope="session")
def response():
    with open('tests/test_spider_item.html', 'r') as f:
        item_html = f.read()
    response = HtmlResponse(url="url-here",
                                body=item_html)
    return response


@pytest.fixture()
def itemspider():
    return ItemSpider()

@pytest.fixture(
    params=[
        {'input':<input-here>,
         'expected': <input-here>},
    ]
)
def link_texts_with_dates(request):
    return request.param


@pytest.fixture(
    params=[
        {'link': <input-here>,
         'expected': <input-here>},
        {'link': <input-here>,
         'expected': <input-here>}
    ]
)
def links(request):
    return request.param


def wait(fn):
    def start_waiting(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (WebDriverException, AssertionError) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return start_waiting


@wait
def wait_for(fn):
    return fn


def test_user_can_login(browser):
    """ Test user login using credentials given """
    login_msg = <input-here>
    assert login_msg in browser.find_element_by_xpath(
        <input-here>).text

# ** Additional tests here ** #