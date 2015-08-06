from requests import Session
from random import choice
import requests



class Optimalstackfacts(object):

    def __init__(self):
        f = open("proxies_808.txt")
        proxies_list = f.readlines()
        self.proxies_url_list = map(self.make_proxy, proxies_list)
        self.headers = self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0'}


    def make_proxy(self, proxie):
        proxie = proxie.strip()
        proxies_split_var = proxie.split()
        ip = proxies_split_var[0].strip()
        port = proxies_split_var[1].strip()

        return "http://%s:%s" %(ip, port)


    def get_url_page(self, url="http://www.optimalstackfacts.org/"):

        for l in xrange(3):
            # proxies_url = choice(self.proxies_url_list)
            proxies_url = "http://82.209.49.200:8080"

            proxies = {
                # "http": "http://eric316:india123@93.127.146.106:80/",
                "http": proxies_url,
                "https": proxies_url

            }

            try:
                session = Session()
                r = session.get(url,  proxies=proxies, headers=self.headers, timeout=10)
                # r = requests.get(url,  proxies=proxies,)
                print r.status_code

                if r.status_code in [200, 301]:

                    page = r.content
                    r.cookies.clear()
                    r.close()

                    return page

                else:
                    r.cookies.clear()
                    r.close()
            except:
                pass



if __name__=="__main__":
    obj = Optimalstackfacts()
    page = obj.get_url_page()
    print



