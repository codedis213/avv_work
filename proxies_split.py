import requests
from random import choice
from requests import Session


class Requests_Proxy(object):

    """
    takes filename
    filename will contain proxies like under

    93.127.146.106:80:eric316:india123
    188.210.215.241:80:eric316:india123

    read file lines into list
    make list of proxy dict with authentication

    call method
    >>> from proxies_split import Requests_Proxy
    >>> obj = Requests_Proxy(filename="proxies_list.txt")
    >>> r = obj.fetch_url(url="https://pypi.python.org/pypi/requests/")
    >>> print r.status_code

    """


    def __init__(self, filename="proxies_list.txt"):
        f = open(filename)
        proxies_list = f.readlines()
        self.proxies_list = map(self.proxies_split_fun, proxies_list)
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0'}


    def proxies_split_fun(self, proxie):
        """
        :param proxie:
        :return:{"ip":ip, "port": port, "username":username, "password":password}
        """
        proxie = proxie.strip()
        proxies_split_var = proxie.split(":")
        ip = proxies_split_var[0]
        port = proxies_split_var[1]
        username = proxies_split_var[2]
        password = proxies_split_var[3]

        return {"ip":ip, "port": port, "username":username, "password":password}


    def make_proxy_url(self):
        """
        :return: proxies_url
        """
        proxies_single_dict = choice(self.proxies_list)
        proxies_url = "http://%s:%s@%s:%s/" %(proxies_single_dict["username"],
                                              proxies_single_dict["password"],
                                              proxies_single_dict["ip"],
                                              proxies_single_dict["port"])
        return proxies_url


    def fetch_url(self, url="https://pypi.python.org/pypi/requests/"):
        """
        :param url:
        :return: request content i.e r
        """

        headers = self.headers

        for l in xrange(3):
            proxies_url = self.make_proxy_url()
            proxies_url = "http://82.209.49.200:8080"
            print proxies_url


            proxies = {
                # "http": "http://eric316:india123@93.127.146.106:80/",
                "http": proxies_url,
                "http": proxies_url

            }

            try:
                # session = Session()
                # r = session.get(url,  proxies=proxies, headers=headers, timeout=5)
                r = requests.get(url,  proxies=proxies,)
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
    obj = Requests_Proxy(filename="proxies_list.txt")
    page = obj.fetch_url(url="http://www.optimalstackfacts.org/")
    # print page