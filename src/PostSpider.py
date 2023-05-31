import requests
from bs4 import BeautifulSoup
import time


def start():
    print("请输入需要爬取的画集的关键字：", end='')
    keyword = input()
    return "https://yande.re/pool?query=" + keyword
