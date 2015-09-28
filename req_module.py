# import requests
from requests import Session
from requests.auth import HTTPProxyAuth
import os
from random import choice
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )


class RequestSet(object):
    """
    obj = RequestSet(pre_dir="mapping_blog", proxy_file="proxies.txt")
    obj.proxy_to_list()
    page = obj.req_module(url)
    return page
    """

    def __init__(self, pre_dir="avv_work", proxy_file="proxies.txt"):
        #self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #self.req_dir = os.path.join(self.base_dir, pre_dir)
        self.f_name = "/root/work_by_jai/avv_work/avv_work/%s" % (proxy_file)
        self.list_of_proxies = None
        self.user = None
        self.password = None
        self.auth = None
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self. session = Session()

    def __del__(self):
        # del self.base_dir
        # del self.req_dir
        # del self.f_name
        del self.list_of_proxies
        del self.user
        del self.password
        del self.auth
        del self.headers
        del self. session



    def proxy_to_list(self):
        with open(self.f_name) as f:
            self.list_of_proxies = f.readlines()

        proxy_str = choice(self.list_of_proxies)
        proxy_str_lst = proxy_str.strip().split(":")
        user, password = proxy_str_lst[2], proxy_str_lst[3]
        self.auth = HTTPProxyAuth(user, password)

    def proxy_spilt(self):
        proxy_str = choice(self.list_of_proxies)
        proxy_str_lst = proxy_str.strip().split(":")
        host = "%s:%s" %(proxy_str_lst[0], proxy_str_lst[1])
        # user, password = proxy_str_lst[2], proxy_str_lst[3]
        return host

    def req_module(self, url):
        for idx in xrange(3):
            host = self.proxy_spilt()

            proxies = {"http": "http://%s/" % host}

            if url.startswith("https:"):
                url = "http://" + url[8:]
                self.headers["x-crawlera-use-https"] = "1"

            try:
                logging.debug(host)

                r = self.session.get(url, headers=self.headers, proxies=proxies, timeout=15,
                                     auth=self.auth, allow_redirects=False)
                page = r.content
                r.close()
                return page

            except:
                pass

        return None


def req_main(url):
    obj = RequestSet(pre_dir="avv_work", proxy_file="proxies.txt")
    obj.proxy_to_list()
    page = obj.req_module(url)
    return page


if __name__ == "__main__":
    url = "http://www.iflscience.com/"
    print req_main(url)
