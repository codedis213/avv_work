from celery import Celery
from requests import Session
from random import choice


app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task(ignore_result=True)
def print_hello():
    print 'hello there'


@app.task
def gen_prime(x):
    multiples = []
    results = []

    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)

            for j in xrange(i*i, x+1, i):
                multiples.append(j)

    return results


@app.task
def get_url_helper(headers, proxies_url_list, url):

        for l in xrange(3):
            proxies_url = choice(proxies_url_list)
            print proxies_url
            # proxies_url = "http://82.209.49.200:8080"
            # proxies_url = "http://eric316:india123@91.108.180.243:80/"

            proxies = {
                "http": proxies_url,
                "https": proxies_url
                }

            try:
                session = Session()

                r = session.get(url,  proxies=proxies, headers=headers, timeout=10)
                # r = requests.get(url,  proxies=proxies,)
                # r = requests.get(url)

                print url
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

        return None


