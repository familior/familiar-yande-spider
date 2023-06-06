import os
import requests
from bs4 import BeautifulSoup
import time


def start():
    print("请输入需要爬取的插画的关键字：", end='')
    keyword = input()
    return keyword


def get_post_download_url_dict(keyword):
    print("开始爬取插画的链接")
    post_url_dict = {}
    response = requests.get("https://yande.re/post?tags=" + keyword)
    first_page = BeautifulSoup(response.text, "lxml")
    paginator = first_page.select_one("#paginator > div > a:nth-last-child(2)")
    if paginator is None:
        last_page_number = 1
    else:
        last_page_number = int(paginator.text)
    print("一共有" + str(last_page_number) + "页插画")

    # 保存第一页的插画url
    print("一共有" + str(last_page_number) + "页插画，" + "爬取第1页的插画链接中...")
    li_list = first_page.select("#post-list-posts > li")
    for li in li_list:
        thumb = li.select_one(".thumb")
        key = thumb.attrs["href"]
        directlink_largeimg = li.select_one(".directlink")
        value = directlink_largeimg.attrs["href"]
        post_url_dict[key] = value

    # 保存其他页的插画url
    for page in range(2, last_page_number + 1):
        time.sleep(1)
        print("一共有" + str(last_page_number) + "页插画，" + "爬取第" + str(page) + "页的插画链接中...")
        response = requests.get("https://yande.re/post?tags=" + keyword + "&page=" + str(page))
        current_page = BeautifulSoup(response.text, "lxml")
        li_list = current_page.select("#post-list-posts > li")
        for li in li_list:
            thumb = li.select_one("a.thumb")
            key = thumb.attrs["href"]
            directlink_largeimg = li.select_one("a.directlink")
            value = directlink_largeimg.attrs["href"]
            post_url_dict[key] = value
    return post_url_dict


def correct_post_download_url(post_download_url_dict):
    tmp = {}
    for key, value in post_download_url_dict.items():
        value_modified = ""
        if "https://files.yande.re/image/" not in value:
            if "https://files.yande.re/jpeg/" in value:
                value_modified = value.replace("https://files.yande.re/jpeg/", "https://files.yande.re/image/", 1) \
                    .replace(".jpg", ".png", 1)
            elif "https://files.yande.re/sample/" in value:
                value_modified = value.replace("https://files.yande.re/sample/", "https://files.yande.re/image/", 1) \
                    .replace("%20sample%20", "%20", 1)
                # 新增一条png的sample改后的image-png组合
                tmp[key+"重复"] = value_modified.replace(".jpg", ".png", 1)
            post_download_url_dict[key] = value_modified
    post_download_url_dict.update(tmp)


def add_to_IDM(post_download_url_dict, path):
    count = 1
    total = len(post_download_url_dict)
    for key, value in post_download_url_dict.items():
        os.system("IDMan /a /d " + value + " /p " + path)
        print("共有" + str(total) + "张插画，" + "第" + str(count) + "张插画添加完毕")
        if count % 8 == 0:
            os.system("IDMan /s")
        count += 1


def crawl_post():
    keyword = start()
    post_download_url_dict = get_post_download_url_dict(keyword)
    with open(keyword + "原始.txt", "w", encoding="utf-8") as f:
        for key, value in post_download_url_dict.items():
            f.write(key + "        " + value + "\n")
    correct_post_download_url(post_download_url_dict)
    # add_to_IDM(post_download_url_dict, "F:\\Downloads\\"+keyword)
    with open(keyword + ".txt", "w", encoding="utf-8") as f:
        for key, value in post_download_url_dict.items():
            f.write(key + "        " + value + "\n")
