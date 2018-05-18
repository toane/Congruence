from socket import gaierror

import urllib3

try:
    from urllib import urlencode
except ImportError as ie:
    from urllib.parse import urlencode
from urllib3 import HTTPSConnectionPool, make_headers, exceptions
import requests


def fetch_url(url, url_args = None):
    print("url :", url)
    try:
        encoded_args = urlencode(url_args)
        request_url = url + encoded_args
    except TypeError as te:
        request_url = url
        pass
    try:
        print("requesting url : ", request_url)
        r = requests.get(request_url, timeout=10)
        return r.text
    except requests.exceptions.ConnectionError as ce:
        print(ce)
    except urllib3.exceptions.MaxRetryError as mre:
        print(mre)

        
        
