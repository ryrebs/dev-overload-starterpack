A. For coding conventions we follow [PEP8](https://www.python.org/dev/peps/pep-0008/)

B. You can also install autopep8 to format your code automatically.

```$pip install autopep8```

C.  Create your files here:
    
    Extensions:
            webscraperapp/extensions/
        And initialize it in __init__.py
    
    Spider:
            webscraperapp/spiders/<media name>/

            e.g
            webscraperapp/
                spiders/
                    media_name/
                        __init__.py
                        spider_name.py

    Models:
            webscraperapp/models/<model_name>.py

            or

            webscraperapp/
                models/
                    <media_name>/
                    __init__.py
                    model_name.py
