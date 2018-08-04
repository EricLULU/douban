import urlparse
import urllib
import random
import time
from datetime import datetime, timedelta
import socket
import requests                #导入requests库
from bs4 import BeautifulSoup  #导入解析库

DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60

class Downloader(object):
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache




    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    result = None
        if result is None:
            #result was not loaded from cache so stil need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-Agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']



    def download(self, url, heades, proxy, num_retries, data=None):
        print("Downloading:", url)
        #开始进行下载
        try:
            r = requests.get(url, headers=headers, proxies=proxy)
            html = r.text
            code = r.status_code
        except Exception as e:
            print('Download error:', str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    return self.downloader(url, headers, proxy, num_retries-1, data)
            else:
                code = None
        return {'html': html, 'code': code}



        
class Throttle(object):
    def __init__(self, delay):
        self.delay = delay
        self.domians = []
    def wait(self, url):
        domain = parse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay = (datetime.now()-last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domain[domian] = datetime.now()
        　
        