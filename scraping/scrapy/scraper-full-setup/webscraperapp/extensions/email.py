from scrapy.mail import MailSender
from scrapy import signals
from scrapy.exceptions import NotConfigured
from collections import namedtuple
import re


class EmailExceptions(object):

    def __init__(self, settings, admins):
        self.settings = settings
        self.admins = admins
        self.Msg = namedtuple('Msg', ['spider', 'error', 'body'])
        self.failures = []

    @classmethod
    def from_crawler(cls, crawler):
        """
        First check if the extension should be enabled and raise
        NotConfigured otherwise
        """
        if not crawler.settings.getbool('CUSTOM_EXT'):
            raise NotConfigured
        # instantiate the extension object
        ext = cls(crawler.settings, crawler.settings.get('MAIL_ADMINS'))
        # connect the extension object to signals
        crawler.signals.connect(ext.send_email, signal=signals.spider_closed)
        crawler.signals.connect(ext.exception_handler,
                                signal=signals.spider_error)
        crawler.signals.connect(ext.error_response_handler,
                                signal=signals.response_received)
        # return the extension object
        return ext

    def error_response_handler(self, response, request, spider):
        error_codes = {
            'Url Not Found': 404,
            'Request Timeout': 408,
            'Internal Server Error': 500,
            'Bad Gateway': 502,
            'Service Unavailable': 503,
            'Gateway Timeout': 504}

        for key, value in error_codes.iteritems():
            if response.status == value:

                if not self.is_failure_duplicate(
                        error=value,
                        body=re.escape(request.url)):
                    self.failures.append(self.Msg(
                        spider=spider.name,
                        error=str(value) + ' ' + key,
                        body='Cannot process response on this url: '
                        + '<b>'
                        + request.url
                        + '</b>')
                    )

    def exception_handler(self, failure, response, spider):
        failure_ = failure.getTraceback().replace('\n', '<br>')
        if not self.is_failure_duplicate(
                'body',
                'error',
                error=failure.getErrorMessage(),
                body=failure_):
            self.failures.append(self.Msg(
                spider=spider.name,
                error=failure.getErrorMessage(),
                body=failure_)
            )

    def send_email(self, spider):
        if self.failures:
            mailer = MailSender.from_settings(self.settings)
            content = u""""""
            for i in self.failures:
                content = content + u"""
                    <div>
                        <h4>Spider name: {}</h4>
                        <span style="color:red;">Error Message: </span>{}
                        <br>
                        <br>
                            {}
                        <br>
                        <hr>
                    </div>
                """.format(i.spider, i.error, i.body)
            html_body = """\
                            <html>
                                <head>
                                </head>
                                <body>
                            {}
                                </body>
                            </html>
                        """.format(content)
            mailer.send(
                to=self.admins,
                subject='Webscraperapp has encountered some issues.',
                body=html_body,
                mimetype='text/html')

    def is_failure_duplicate(self, *exact, **kwargs):
        """
        kwargs contains the search values
        search only in these properties: error and body
        exact  contains search values for matching the whole text
        """
        for f in self.failures:
            # Compare body and error
            # against existing failures
            exact_body = kwargs.get('body') == f.body
            exact_error = kwargs.get('error') == f.error

            # Match only the part of body and error
            # against existing failures
            match_error = re.search(
                str(kwargs.get(
                    'error')),
                f.error) if 'error' not in exact else exact_error

            match_body = re.search(
                kwargs.get('body'), f.body,
                re.IGNORECASE) if 'body' not in exact else exact_body

            if match_error and match_body:
                return True

        return False
