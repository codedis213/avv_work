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

                for a in all_a:
                    link = "http://www.highya.com%s" % a.get("href")
                    page2 = req_main(url)

                    if page2:
                        soup2 = BeautifulSoup(page2)
                        article_tag = soup2.find("article", attrs={"class":"product-article"})

                        if article_div:
                            header = article_tag.find("header")
                            domain = "www.highya.com"
                            main_title = soup2.find("title").text()
                            main_title_link = link
                            article_div = article_tag.find("div", attrs={"class":"site-section section-article"})
                            blog_title = article_div.find("h2").text()
                            blog_link = link
                            itemtype = header.get("itemtype").split("/")[-1]
                            category = itemtype
                            cat_link = link
                            entry_content = article_div
                            entry_text = article_div.text()

if __name__=="__main__":
    parse_url(url="http://www.highya.com/")



