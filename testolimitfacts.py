import requests
from bs4 import BeautifulSoup
import MySQLdb
from datetime import datetime
from req_proxy import main_req
from req_module import req_main


class TesToLimitFacts(object):

    def __init__(self):
        self.domain_name = "testolimitfacts"
        self.domain_link = "http://testolimitfacts.com/"
        self.db = MySQLdb.connect("localhost", "root", "rootavv", "avv_blog_scrap" )
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

        sql_email_rows = """select email from avv_blog_email_handling_table"""
        self.cursor.execute(sql_email_rows)
        email_rows = self.cursor.fetchall()


        self.to = [em[0] for em in email_rows]
        self.to.extend(["jaiprakashsingh213@gmail.com", 'santosh.kumar@wisepromo.com' ])


    def req_proxy(self, proxy_ip= "14.152.49.194:8080", link= "http://www.healthyminimarket.com"):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0'}
        http_proxy = "http://%s" % proxy_ip
        print http_proxy
        proxyDict = {"http": http_proxy, "https": http_proxy}
        r = requests.get(link,  proxies= proxyDict, headers= headers, timeout= 20)
        # r = requests.get(link)
        print r.status_code
        return r



    def get_link_from_first_page(self, link, page):
        soup = BeautifulSoup(page, "html.parser")
        main_title_text= soup.find("h1", {"class": "entry-title"}).get_text()
        main_title_link = link
        post_title_text = main_title_text
        post_title_link = main_title_link

        category_link = soup.find("a", {"rel":"category tag"}).get("href")
        category = soup.find("a", {"rel":"category tag"}).get_text()

        entry_content_div = soup.find("div", {"class":"entry-content"})
        entry_content_text = soup.find("div", {"class":"entry-content"}).get_text()


        sql = """SELECT * FROM avv_blog_scrap_table WHERE blog_title = '%s' """ % (self.my_strip(post_title_text))
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        if not results:

            sql = """INSERT INTO avv_blog_scrap_table
                    (domain_name, domain_link, main_title, main_title_link,
                    blog_title, blog_link, category_title, category_link,
                    sub_category_title, sub_category_link,
                    entry_content_html, entry_content_text, created_on, changed_on)
                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

            extracted_data = (self.domain_name, self.domain_link, main_title_text,
                              main_title_link, post_title_text, post_title_link,
                              category, category_link, '', '', entry_content_div,
                              entry_content_text,
                              datetime.now(), datetime.now())

            extracted_data = map(self.my_strip, extracted_data)
            sql = sql % tuple(extracted_data)

            commited = False


            try:
                self.cursor.execute(sql)
                self.db.commit()
                commited = True
                print "entered............"
            except:
                self.db.rollback()
                print"rollback........"


            if commited:
                # to = ["jaiprakashsingh213@gmail.com", "santosh.kumar@wisepromo.com "]
                to = self.to
                subject = "new blog on %s with title %s" %(self.domain_name, post_title_text)
                message = """Hi
                            "new blog on %s
                            whose details are under follow
                            title ==> %s
                            link ==> %s"""
                message = message %(self.domain_name, post_title_text, post_title_link)

                self.send_simple_message(to, subject, message)
                print "maill sent "


    def home_page_link(self):
        self.creat_avv_blog_scrap_table()

        # r = self.req_proxy()
        # page = r.content
        # r.close()

        link_list = ["http://testolimitfacts.com/",
                      # "http://testolimitfacts.com/testo-limit-review/",
                      #   "http://testolimitfacts.com/testo-limit-review/",
                      #   "http://testolimitfacts.com/slimgenix-pro/",
                      #   "http://testolimitfacts.com/power-pro/",
                      #   "http://testolimitfacts.com/addium-brain-enhancer-another-scam/",
                      #   "http://testolimitfacts.com/enduros-male-enhancement/",
                      #   "http://testolimitfacts.com/testo-xl/",
                      #   "http://testolimitfacts.com/is-spartagen-xt-scam/",
                      #   "http://testolimitfacts.com/elite-test-360/",
                      #   "http://testolimitfacts.com/honest-green-coffee-bean-extract/",
                      #   "http://testolimitfacts.com/premium-natural-garcinia-cambogia/",
                      #   "http://testolimitfacts.com/maximum-shred/",
                      #   "http://testolimitfacts.com/extreme-home-profits-review-worth-the-money-or-a-scam/",
                      #   "http://testolimitfacts.com/30-day-change/",
                      #   "http://testolimitfacts.com/100-day-loans/",
                     ]

        for link in link_list:
            # page = main_req(link)
            page = req_main(link)

            if page:
                self.get_link_from_first_page(link, page)


if __name__ == "__main__":
    obj = TesToLimitFacts()
    obj.home_page_link()

