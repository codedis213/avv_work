import requests
from bs4 import BeautifulSoup
import MySQLdb
from datetime import datetime
from req_proxy import main_req


class HealthyMiniMarket(object):


    def __init__(self):
        self.domain_name = "healthyminimarket"
        self.domain_link = "http://www.healthyminimarket.com"
        self.db = MySQLdb.connect("localhost", "root", "root", "avv_blog_scrap" )
        self.cursor = self.db.cursor()


    def __del__(self):
        self.db.close()


    def send_simple_message(self, to, subject, message):
        return requests.post(
            "https://api.mailgun.net/v3/sandboxa87eb15ddb8c420d87d5c8db15f80a69.mailgun.org/messages",
            auth=("api", "key-761deed87c5ec92e3372b3a4747df079"),
            data={"from": "Excited User <mailgun@sandboxa87eb15ddb8c420d87d5c8db15f80a69.mailgun.org>",
                  "to": to,
                  "subject": subject,
                  "text": message})


    def my_strip(self, x):
        try:
            x = self.db.escape_string(x)
        except:
            try:
                x = str(x).strip()
            except:
                x = str(x.encode("ascii", "ignore")).strip()
                x = self.db.escape_string(x)

        return x


    def creat_avv_blog_scrap_table(self):
        sql_stmnt = """CREATE TABLE IF NOT EXISTS avv_blog_scrap_table (
                          id int(11) NOT NULL AUTO_INCREMENT,
                          domain_name varchar(70) DEFAULT NULL,
                          domain_link  varchar(255) DEFAULT NULL,
                          main_title varchar(100) DEFAULT NULL,
                          main_title_link varchar(255) DEFAULT NULL,
                          blog_title varchar(100) DEFAULT NULL,
                          blog_link varchar(255) DEFAULT NULL,
                          category_title varchar(100) DEFAULT NULL,
                          category_link varchar(255) DEFAULT NULL,
                          sub_category_title varchar(100) DEFAULT NULL,
                          sub_category_link varchar(255) DEFAULT NULL,
                          entry_content_html longtext NOT NULL,
                          entry_content_text longtext NULL,
                          created_on TIMESTAMP DEFAULT 0,
                          changed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                          PRIMARY KEY (id)
                        )"""

        self.cursor.execute(sql_stmnt)


    def req_proxy(self, proxy_ip= "14.152.49.194:8080", link= "http://www.healthyminimarket.com"):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0'}
        http_proxy = "http://%s" % proxy_ip
        print http_proxy
        proxyDict = {"http": http_proxy, "https": http_proxy}
        r = requests.get(link,  proxies= proxyDict, headers= headers, timeout= 20)
        # r = requests.get(link)
        print r.status_code
        return r


    def get_detail_next_page(self, link, page2):
        soup2 = BeautifulSoup(page2, "html.parser")

        crumbs_div = soup2.find("div", {"id":"crumbs"})
        crumbs_all_a = crumbs_div.find_all("a")

        if crumbs_all_a.__len__() == 3:
            category= crumbs_all_a[1].get_text()
            category_link = crumbs_all_a[1].get("href")
            sub_category= crumbs_all_a[2].get_text()
            sub_category_link = crumbs_all_a[2].get("href")


        elif crumbs_all_a.__len__() == 2:
            category= crumbs_all_a[1].get_text()
            category_link = crumbs_all_a[1].get("href")
            sub_category= ''
            sub_category_link = ''

        else:
            category= ''
            category_link = ''
            sub_category= ''
            sub_category_link = ''

        blog_title_div = soup2.find("h1", {"class":"entry-title"})

        main_title_text = blog_title_div.find("a").get("href")
        main_title_link = blog_title_div.find("a").get_text()
        post_title_link = blog_title_div.find("a").get("href")
        post_title_text = blog_title_div.find("a").get_text()

        entry_content_div = soup2.find("span", {"itemprop":"articleBody"})
        entry_content_text = soup2.find("span", {"itemprop":"articleBody"}).get_text()

        sql = """INSERT INTO avv_blog_scrap_table
                (domain_name, domain_link, main_title, main_title_link,
                blog_title, blog_link, category_title, category_link,
                sub_category_title, sub_category_link,
                entry_content_html, entry_content_text, created_on, changed_on)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

        extracted_data = (self.domain_name, self.domain_link, main_title_text,
                          main_title_link, post_title_text, post_title_link,
                          category, category_link, sub_category, sub_category_link,
                          entry_content_div,
                          entry_content_text, datetime.now(), datetime.now())

        extracted_data = map(self.my_strip, extracted_data)
        sql = sql % tuple(extracted_data)

        commited = False

        self.cursor.execute(sql)
        self.db.commit()

        try:
            self.cursor.execute(sql)
            self.db.commit()
            commited = True
            print "entered............"
        except:
            self.db.rollback()
            print"rollback........"


        if commited:
            to = ["jaiprakashsingh213@gmail.com", 'santosh.kumar@wisepromo.com' ]
            subject = "new blog on %s with title %s" %(self.domain_name, post_title_text)
            message = """Hi
                        "new blog on %s
                        whose details are under follow
                        title ==> %s
                        link ==> %s"""
            message = message %(self.domain_name, post_title_text, post_title_link)

            self.send_simple_message(to, subject, message)
            print "maill sent "


    def get_page_next_link(self, link):
        sql = """SELECT * FROM avv_blog_scrap_table WHERE blog_link = '%s' """ % (self.my_strip(link))
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        if not results:
            # r2 = self.req_proxy(link=link)
            # page2 = r2.content
            # r2.close()

            page2 = main_req(link)

            if page2:
                self.get_detail_next_page(link, page2)


    def get_link_from_first_page(self, page):
        soup = BeautifulSoup(page, "html.parser")

        h2_div_list = soup.find_all("h2", {"class":"entry-title"})

        all_link_home_page = [h2_obj.find("a").get("href") for h2_obj in h2_div_list]
        map(self.get_page_next_link, all_link_home_page)


    def home_page_link(self):
        self.creat_avv_blog_scrap_table()

        # r = self.req_proxy()
        # page = r.content
        # r.close()

        link_list = ["http://www.healthyminimarket.com",
                     "http://www.healthyminimarket.com/page/2/",
                     "http://www.healthyminimarket.com/page/3/",
                     "http://www.healthyminimarket.com/page/4/",
                     "http://www.healthyminimarket.com/page/5/",
                     "http://www.healthyminimarket.com/page/6/",
                     "http://www.healthyminimarket.com/page/7/",
                     "http://www.healthyminimarket.com/page/8/",
                     "http://www.healthyminimarket.com/page/9/",
                     "http://www.healthyminimarket.com/page/10/",
                     "http://www.healthyminimarket.com/page/11/",
                     "http://www.healthyminimarket.com/page/12/",
                     "http://www.healthyminimarket.com/page/13/",
                     "http://www.healthyminimarket.com/page/15/",
                     "http://www.healthyminimarket.com/page/16/"]

        for link in link_list:
            page = main_req(link)

            if page:
                self.get_link_from_first_page(page)


if __name__ == "__main__":
    obj = HealthyMiniMarket()
    obj.home_page_link()

