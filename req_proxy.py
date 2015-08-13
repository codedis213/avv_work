from requests import Session
from random import choice
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')


def main_req(link):
    f = open("proxies_808.txt")
    pass_ip_list = f.readlines()
    f.close()

    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0'}

    for l in xrange(2):
        pass_ip = choice(pass_ip_list)
        pass_ip = pass_ip.strip()

        try:
            http_proxy = "http://" + pass_ip + ":8080"

            proxyDict = {"http": http_proxy,
                         "https": http_proxy
                         }
            #r = requests.get(link,  proxies = proxyDict, headers=headers, timeout = 5)
            session = Session()
            r = session.get(link,  proxies = proxyDict, headers=headers, timeout = 15)

            if r.status_code in range(200,399):
                page = r.content
                logging.debug(r.status_code)
                r.cookies.clear()

                r.close()
                return page

            else:
                r.cookies.clear()
                r.close()

        except:
            pass

    return None


if __name__ == "__main__":
    link = "http://www.flipkart.com/united-colors-benetton-men-s-solid-casual-shirt/p/itmdvjfhuknafbsv?pid=SHTDTH99CD9CUAY4&srno=b_1&ref=aee8d63b-38ab-4d95-b96f-9d930f81c548"
    page = main_req(link)
    print page
