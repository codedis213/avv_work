# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import logging
from random import choice


class OpenProxyFile(object):

    def __init__(self):
        self.directory_path = "/home/rrvc/jai_practice/avv_work/tutorial/tutorial"
        self.filename = "%s/proxies.txt" % self.directory_path
        with open(self.filename) as f:
            self.list_of_proxies = f.readlines()


# Start your middleware class
class ProxyMiddleware(OpenProxyFile):

    def __init__(self):
        OpenProxyFile.__init__(self)

    # overwrite process request
    def process_request(self, request, spider):

        proxy_str = choice(self.list_of_proxies)
        proxy_str_lst = proxy_str.strip().split(":")
        host = "%s:%s" %(proxy_str_lst[0], proxy_str_lst[1])
        user, password = proxy_str_lst[2], proxy_str_lst[3]

        # Set the location of the proxy
        request.meta['proxy'] = "http://%s" % host

        # Use the following lines if your proxy requires authentication
        proxy_user_pass = "%s:%s" %(user, password)
        # setup basic authentication for the proxy
        logging.debug("http://%s" % host)
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass