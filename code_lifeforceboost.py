from requests import Session
from random import choice
import requests



class lifeforceboost(object):
    """
    >>> obj = lifeforceboost()
    >>> obj.get_url_page()

    """

    def __init__(self):
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


    def get_url_page(self, url="http://www.lifeforceboost.com/"):

        for l in xrange(3):
            proxies_url = choice(self.proxies_url_list)
            proxies_url = "http://82.209.49.200:8080"
            # proxies_url = "http://eric316:india123@91.108.180.243:80/"
            print proxies_url


            proxies = {
                # "http": "http://eric316:india123@93.127.146.106:80/",
                "http": proxies_url,
                "https": proxies_url
            }

            try:
                session = Session()
                r = session.get(url,  proxies=proxies, headers=self.headers, timeout=20)
                # r = requests.get(url,  proxies=proxies,)
                # r = requests.get(url)
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
    obj = lifeforceboost()
    page = obj.get_url_page()
    print page



