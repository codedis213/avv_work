from requests import Session
from random import choice
import requests
from bs4 import BeautifulSoup
# from tasks import *
from helper import *
import logging
import time
import multiprocessing


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

num_fetch_threads = 20
enclosure_queue = multiprocessing.JoinableQueue()


class healthcare(object):
    """

    >>> obj = healthcare()
    >>> obj.get_url_page()

    """


    def __init__(self):
        self.recent_link = []

        f = open("proxies_808.txt")
        proxies_list = f.readlines()

        self.proxies_url_list = map(self.make_proxy, proxies_list)

        self.headers = {"Connection":"keep-alive",
                        "Content-Encoding":"gzip",
                        "Content-Length":	"5981",
                        "Content-Type": "text/html; charset=UTF-8",
                        "Date":"Thu, 06 Aug 2015 09:25:27 GMT",
                        "Server":"nginx/1.9.3",
                        "Vary"	:"User-Agent,Accept-Encoding",
                        "X-Pingback" : "http://www.optimalstackfacts.org/xmlrpc.php",
                        "X-Powered-By": "PHP/5.4.43, PleskLin",
                        "Request" : "Headersview source",
                        "Accept" :	"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language" :	"en-US,en;q=0.5",
                        "Cache-Control" : "max-age=0",
                        "Connection" : "keep-alive",
                        "Host" :"www.optimalstackfacts.org",
                        "Referer" : "http://www.optimalstackfacts.org/",
                        "User-Agent" :"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0"}

        self.headers = {"User-Agent" :"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0"}


    def make_proxy(self, proxie):
        proxie = proxie.strip()

        proxies_split_var = proxie.split()

        ip = proxies_split_var[0].strip()
        port = proxies_split_var[1].strip()

        return "http://%s:%s" %(ip, port)


    def get_url_page(self, url="http://www.healthcaresdiscussion.com/"):
        # page_return = get_url_helper.delay(self.headers, self.proxies_url_list, url)
        # print page_return.get()
        page_return = get_url_helper(self.headers, self.proxies_url_list, url)

        if page_return:
            self.get_home_soup(page_return)


    def get_home_soup(self, page):
        soup = BeautifulSoup(page, 'html.parser')

        all_title = soup.find_all("h2", {"class":"post-title"})
        self.recent_link.extend([h2_post_tile.find("a").get("href") for h2_post_tile  in all_title])


def mainthread2(i, q):
    for obj, link in iter(q.get, None):
        try:
            obj.get_url_page(url=link)
            logging.debug(link)
        except:
            pass

        time.sleep(2)
        q.task_done()

    q.task_done()


def supermain():
    obj = healthcare()

    link_list = ["http://www.healthcaresdiscussion.com/page/3/",
                "http://www.healthcaresdiscussion.com/page/2/",
                "http://www.healthcaresdiscussion.com"]

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=mainthread2, args=(i, enclosure_queue,)))
        procs[-1].start()

    for link in link_list:
        enclosure_queue.put((obj, link))
        enclosure_queue.join()

    for p in procs:
        enclosure_queue.put(None)
        enclosure_queue.join()

    for p in procs:
        p.join(120)


if __name__=="__main__":
    supermain()