import requests
from stem import Signal
from stem.control import Controller

def new_tor_ip():
    with Controller.from_port(port=9051) as c:
        c.authenticate()
        c.signal(Signal.NEWNYM)

def make_request(url):
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    return requests.get(url, proxies=proxies)