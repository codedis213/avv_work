import requests
from random import choice

f = open("proxies_list.txt")
proxies_list = f.readlines()

def proxies_split_fun(proxie):
    proxie = proxie.strip()
    proxies_split_var = proxie.split(":")
    ip = proxies_split_var[0]
    port = proxies_split_var[1]
    username = proxies_split_var[2]
    password = proxies_split_var[3]

    return {"ip":ip, "port": port, "username":username, "password":password}



proxies_list = map(proxies_split_fun, proxies_list)

proxies_single_dict = choice(proxies_list)
proxies_url = "http://%s:%s@%s:%s/" %(proxies_single_dict["username"],
                                      proxies_single_dict["password"],
                                      proxies_single_dict["ip"],
                                      proxies_single_dict["port"])

print proxies_url

proxies = {
    # "http": "http://eric316:india123@93.127.146.106:80/",
    "http": proxies_url,
    "http": proxies_url

}


r = requests.get("https://pypi.python.org/pypi/requests/", proxies=proxies)
print r.status_code