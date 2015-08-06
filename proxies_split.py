import requests

f = open("proxies_list.txt")
proxies_list = f.readlines()

print proxies_list

def proxies_split_fun(proxie):
    proxie = proxie.strip()
    print proxie
    proxies_split_var = proxie.split(":")
    print proxies_split_var
    ip = proxies_split_var[0]
    port = proxies_split_var[1]
    username = proxies_split_var[2]
    password = proxies_split_var[3]

    print {"ip":ip, "port": port, "username":username, "password":password}



map(proxies_split_fun, proxies_list)


proxies = {
    "http": "http://eric316:india123@93.127.146.106:80/"
}


r = requests.get("https://pypi.python.org/pypi/requests/", proxies=proxies)
print r.status_code