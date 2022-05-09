# -*- coding: utf-8 -*-

from functools import wraps
import re
import os
from datetime import datetime

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(os.path.dirname(APP_DIR), 'temp')
HR = datetime.utcnow().strftime('%H')
MIN = datetime.utcnow().strftime('%M')
SECS = datetime.utcnow().strftime('%S')
DATA = {
    'sample_data': {},
    'sample_data_2': 0
}


def save_to_file(item, name):
    _datetime = datetime.utcnow().strftime(
        '%y-%d-%m({}-{}-{})').format(HR, MIN, SECS)
    _path = os.path.join(TEMP_DIR, '{0}_{1}_file.txt'.format(_datetime, name))

    with open(_path, 'a+') as (f):
        for key, value in item.iteritems():
            print key
            f.write(str(key.encode(u'utf-8')) + ':' +
                    str((u'').join(value).encode('utf-8')))
            f.write('\n')

        f.write('------------------------------------\n')
        f.write('------------------------------------\n')


def exportAsText(fn):
    
    @wraps(fn)
    def wrapper(*args, **kwargs):
        spider = args[2]
        item = args[1]

        ## Insert logic

        return fn(*args, **kwargs)

    return wrapper


def exportAsText(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        spider = args[2]
        item = args[1]

         ## Insert logic

        return fn(*args, **kwargs)

    return wrapper


def filterEmptyFieldsAsText(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        spider = args[2]
        item = args[1]

        ## Insert logic

        return fn(*args, **kwargs)

    return wrapper
