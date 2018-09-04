import requests
from zhihu import settings


def get_ip():
    return requests.get(settings.IP_POOL_GET_URL).text


def del_ip():
    requests.get(settings.IP_POOL_DEL_URL)
