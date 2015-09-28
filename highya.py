import requests
from bs4 import BeautifulSoup
import MySQLdb
from datetime import datetime
from req_proxy import main_req
from req_module import req_main
import re




def parse_url(url="http://www.highya.com/"):
    page = req_main(url)
    if page:
        soup = BeautifulSoup(page)
        latest_reviews_h3 = soup.find("h3", text=re.compile("latest reviews:"))

        if latest_reviews_h3:
            post_div = latest_reviews_h3.find_next("div", attrs={"class":"clearfix like-right-col"})

            if post_div:
                all_li = post_div.find_all("li")
                all_a = [li.find("a") for li in all_li]

                f = open("all_a_list", "w+")
                for a in all_a:
                    link = "http://www.highya.com%s" % a.get("href")
                    f.write(link + "\n")
                f.close()


if __name__=="__main__":
    parse_url(url="http://www.highya.com/")



