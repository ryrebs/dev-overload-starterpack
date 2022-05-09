### Basic commands
---

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

---

##### Please visit: http://scrapyd.readthedocs.io/en/latest/api.html for more info