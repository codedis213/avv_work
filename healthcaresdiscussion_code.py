import requests
from bs4 import BeautifulSoup
import MySQLdb


class HealthCaresDiscussion(object):


    def __init__(self):
        self.domain_name = "healthcaresdiscussion"
        self.domain_link = "http://www.healthcaresdiscussion.com/"
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
            x = str(x).strip()
            # x = str(x.encode("ascii", "ignore")).strip()
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
                          entry_content text DEFAULT NULL,
                          created_on TIMESTAMP DEFAULT 0,
                          changed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                          PRIMARY KEY (id)
                        )"""

        self.cursor.execute(sql_stmnt)


    def req_proxy(self, proxy_ip= "77.245.110.213:8080", link= "http://www.healthcaresdiscussion.com/"):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0'}
        http_proxy = "http://%s" % proxy_ip
        print http_proxy
        proxyDict = {"http": http_proxy, "https": http_proxy}

        r = requests.get(link,  proxies= proxyDict, headers= headers, timeout= 20)
        # r = requests.get(link)
        print r.status_code
        return r


    @staticmethod
    def get_all_link_home_page(page):
        soup = BeautifulSoup(page, "html.parser")
        h2_list = soup.find_all("h2", {"class": "post-title"})

        link_to_extract = [h2.find("a").get("href") for h2 in h2_list]

        return link_to_extract


    def get_detail_next_page(self, link, page2):
        soup2 = BeautifulSoup(page2, "html.parser")
        main_div = soup2.find("div", {"id": "main"})
        primary_div = main_div.find("div",  {"id": "primary"})

        main_title_div = soup2.find("h1", {"id":"title"})
        main_title_link = main_title_div.find("a").get("href")
        main_title_text = main_title_div.find("a").get_text()

        post_title_div = primary_div.find("h2", {"class": "post-title"})
        post_title_link = post_title_div.find("a").get("href")
        post_title_text = post_title_div.find("a").get_text()

        category_div = primary_div.find("a", {"rel": "category tag"})
        category_link = category_div.get("href")
        category = category_div.get_text()

        entry_content_div = primary_div.find("div", {"class":"entry-content"})


        sql = """INSERT INTO avv_blog_scrap_table
                (domain_name, domain_link, main_title, main_title_link,
                blog_title, blog_link, category_title, category_link,
                sub_category_title, sub_category_link,
                entry_content)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

        extracted_data = (self.domain_name, self.domain_link, main_title_text,
                          main_title_link, post_title_text, post_title_link,
                          category, category_link, '', '', entry_content_div)

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
            to = ["jaiprakassingh213@gmail.com"]
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
            r2 = self.req_proxy(link=link)
            page2 = r2.content
            r2.close()
            self.get_detail_next_page(link, page2)


    def open_home_page(self):
        self.creat_avv_blog_scrap_table()
        r = self.req_proxy()
        page = r.content
        r.close()

        link_to_extract = self.get_all_link_home_page(page)

        map(self.get_page_next_link, link_to_extract)


if __name__ == "__main__":
    obj = HealthCaresDiscussion()
    obj.open_home_page()


