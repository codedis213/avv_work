import requests
from random import choice


class Requests_Proxy(object):

    """
    takes filename
    filename will contain proxies like under

    93.127.146.106:80:eric316:india123
    188.210.215.241:80:eric316:india123

    read file lines into list
    make list of proxy dict with authentication

    call method

    >>> obj = Requests_Proxy(filename="proxies_list.txt")
    >>> r = obj.fetch_url(url="https://pypi.python.org/pypi/requests/")
    >>> print r.status_code

    """


    def __init__(self, filename="proxies_list.txt"):
        f = open(filename)
        proxies_list = f.readlines()
        self.proxies_list = map(self.proxies_split_fun, proxies_list)


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
        self.proxies_url = "http://%s:%s@%s:%s/" %(proxies_single_dict["username"],
                                              proxies_single_dict["password"],
                                              proxies_single_dict["ip"],
                                              proxies_single_dict["port"])


    def fetch_url(self, url="https://pypi.python.org/pypi/requests/"):
        """
        :param url:
        :return: request content i.e r
        """
        self.make_proxy_url()
        proxies_url = self.proxies_url

        print proxies_url

        proxies = {
            # "http": "http://eric316:india123@93.127.146.106:80/",
            "http": proxies_url,
            "http": proxies_url

        }

        r = requests.get(url, proxies=proxies)
        print r.status_code
        return r




if __name__=="__main__":
    obj = Requests_Proxy(filename="proxies_list.txt")
    r = obj.fetch_url(url="https://pypi.python.org/pypi/requests/")
    print r.status_code