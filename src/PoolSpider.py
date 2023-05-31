import os

import requests
from bs4 import BeautifulSoup
import time


def start():
    print("请输入需要爬取的画集的关键字：", end='')
    keyword = input()
    return "https://yande.re/pool?query=" + keyword


def get_pool_url_dict(url):
    print("开始爬取画集的链接")
    pool_url_dict = {}
    response = requests.get(url)
    first_page = BeautifulSoup(response.text, "lxml")
    paginator = first_page.select_one("#paginator > div > a:nth-last-child(2)")
    if paginator is None:
        last_page_number = 1
    else:
        last_page_number = int(paginator.text)

    # 保存第一页的画集url
    tr_list = first_page.select("#pool-index > table > tbody > tr")
    for tr in tr_list:
        a_label = tr.select_one("td > a")
        key = a_label.text
        value = a_label.attrs["href"]
        pool_url_dict[key] = "https://yande.re" + value

    # 保存其他页的画集url
    for page in range(2, last_page_number + 1):
        time.sleep(1)
        response = requests.get(url + "&page=" + str(page))
        current_page = BeautifulSoup(response.text, "lxml")
        tr_list = current_page.select("#pool-index > table > tbody > tr")
        for tr in tr_list:
            a_label = tr.select_one("td > a")
            key = a_label.text
            value = a_label.attrs["href"]
            pool_url_dict[key] = "https://yande.re" + value

    return pool_url_dict


def get_post_url_dict(pool_url_dict):
    print("开始爬取图片的链接")
    post_url_dict = {}
    for key, value in pool_url_dict.items():
        time.sleep(1)
        post_url_list = []
        soup = BeautifulSoup(requests.get(value).text, "lxml")
        li_list = soup.select("#post-list-posts > li")
        count = 1
        for li in li_list:
            print("正在爬取画集" + str(key) + "的第" + str(count) + "张图片的链接")
            count += 1
            post_url = li.select_one("a").attrs["href"]
            post_url_list.append("https://yande.re" + post_url)
        post_url_dict[key] = post_url_list
    return post_url_dict


def get_post_download_url_dict(post_url_dict):
    print("开始爬取图片的下载链接")
    post_download_url_dict = {}
    for key, value in post_url_dict.items():
        post_list = []
        count = 1
        for post in value:
            time.sleep(1)
            print("正在爬取画集" + str(key) + "的第" + str(count) + "张图片的下载链接")
            count += 1
            soup = BeautifulSoup(requests.get(post).text, "lxml")
            a_png = soup.select_one("#png")
            a_jpg = soup.select_one("#highres")
            if a_png is not None:
                post_list.append(a_png.attrs["href"])
            else:
                post_list.append(a_jpg.attrs["href"])
        post_download_url_dict[key] = post_list
    return post_download_url_dict


def batch_download(post_download_url_dict):
    print("开始下载...")
    for key, value in post_download_url_dict.items():
        if not os.path.exists(key):
            os.mkdir(key)
        count = 1
        for post in value:
            time.sleep(1)
            print("下载画集" + key + "的第" + str(count) + "张图片中...")
            filename = ".//" + key + "//" + str(count) + post[-4:]
            if os.path.exists(filename):
                print("画集" + key + "的第" + str(count) + "张图片已存在")
                continue
            response = requests.get(post).content
            with open(filename, mode='wb') as f:
                f.write(response)
            count += 1


def crawl_pool():
    url = start()
    print("初始url获取完毕---------------------------------------------------")
    pool_url_dict = get_pool_url_dict(url)
    print("画集url获取完毕---------------------------------------------------")
    post_url_dict = get_post_url_dict(pool_url_dict)
    print("画集内图片链接获取完毕-----------------------------------------------")
    post_download_url_dict = get_post_download_url_dict(post_url_dict)
    print("画集内图片下载链接获取完毕--------------------------------------------")
    batch_download(post_download_url_dict)
    print("下载完毕---------------------------------------------------------")
    input()
