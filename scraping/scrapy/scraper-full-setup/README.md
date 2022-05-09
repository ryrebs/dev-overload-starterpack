### WEBSCRAPERAPP

A Sample Web Scraper setup using the Scrapy framework.

A. Getting started

```
scrapy crawl <spider_name>
```

B. Prerequisites

    Main components are:
        Python 2.7.6
        Scrapy 1.5.0
        Scrapyd 1.2.0
        Scrapyd-client 1.1.0

C. Installing

1. Install and activate virtualenv

```
    $pip install virtualenv

    $virtualenv -p <python-version> <your virtualenv>

    $./<your virtualenv>/bin/activate
```

2. Install scrapy and other requirements

3. Run spider for supported media

```
    $scrapy crawl <spider name>
```

D. Running the tests

`$python -m pytest`

e.g Functional test  
**\*Install chromedriver in your system to pass the functional test**

Test if the user can login with the defined credentials.

            def test_user_can_login(browser):
                login_msg = u'Welcome'
                assert login_msg in browser.find_element_by_xpath(
                "//div[@class='flash-messages']/div").text

### Deployment

scrapy.cfg:

    [settings]
    default = webscraperapp.settings

    [deploy:test]
    url = <url>:<port>
    project = webscraperapp


    [deploy:production]
    url = <url>:<port>
    username = <username>
    password = <password>
    project = webscraperapp

Deploy the app with:

`$ scrapyd-deploy <production, staging, test> -p webscraperapp --version GIT`

---

### Built with:

[Scrapy 1.5.0](https://scrapy.org/)

_Check the documentations for more info._

### Contributing

Please read CONTRIBUTING.md for details.

### Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the tags on this repository

### Authors

- <author>

### License

### Acknowledgments

---

### Todos

- [x] Port existing codebase to Python 3.

### Common Commands on Scrapyd

### Please visit: http://scrapyd.readthedocs.io/en/latest/api.html for more info

### List all projects

    $ curl 192.168.99.100:32768/listprojects.json
    $ curl http://localhost:6800/listprojects.json

### List versions

    $ curl http://localhost:6800/listversions.json?project=myproject

### List spiders

    $ curl http://localhost:6800/listspiders.json?project=myproject

### List jobs

### Also shows the job id

    $  curl http://localhost:6800/listjobs.json?project=myproject | python -m json.tool

### Cancelling spider jobs

    $ curl http://localhost:6800/cancel.json -d project=myproject -d job=6487ec79947edab326d6db28a2d86511e8247444

### Del project

    $ curl http://localhost:6800/delproject.json -d project=myproject

### Daemon status

    $ curl http://localhost:6800/daemonstatus.json

### Scheduling

    Parameters:
    project (string, required) - the project name
    spider (string, required) - the spider name
    setting (string, optional) - a Scrapy setting to use when running the spider
    jobid (string, optional) - a job id used to identify the job, overrides the default generated UUID
    _version (string, optional) - the version of the project to use
    any other parameter is passed as spider argument

    $ curl http://localhost:6800/schedule.json -d project=myproject -d spider=somespider

### Automatic egg building and deployment with scrapyd-deployment

    $ scrapyd-deploy -p <project-name>
    $ scrapyd-deploy <target> -p <project-name>
    $ scrapyd-deploy <target> -p <project> --version <version>

### deploy with scrapyd-deploy with versioning

    $ scrapyd-deploy production -p webscraperapp --version GIT
    $ scrapyd-deploy staging -p webscraperapp --version GIT
    $ scrapyd-deploy test -p webscraperapp --version v1.0.3a-test

### tagging

    git tag -f -a <tag> -m <annotation>
    -f = force, update
    -a = tag
    -m = message, annotation

### egg deployment to prod

    rm -rf build dist webscraperapp.egg-info;
    python setup.py test bdist_egg;
    curl http://<url-here>:6800/delproject.json -d project=webscraperapp;
    curl http://<url-here>:6800/addversion.json -F project=webscraperapp -F version=r1.0.3  -F egg=@dist/webscraperapp-1.0.3-py2.7.egg;

    curl -u user:pass http://<url-here>:32768/delproject.json -d project=webscraperapp;
    scrapyd-deploy test -p webscraperapp --version v1.0.4;

### set system encoding to utf-8

from scrapy.mail import MailSender
import sys

reload(sys)  
sys.setdefaultencoding('utf8')
