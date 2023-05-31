import requests
from bs4 import BeautifulSoup
import time


def welcome():
    print('欢迎使用芙咪莉娅的Yande图片批量爬取器')
    print('B站：芙咪莉娅')
    print('')
    print('tags来自Yande，请先确定要批量下载的图片的tags')
    print('请输入待爬取的tags：', end='')
    tags = input()
    return tags


def get_the_number_of_page(tags):
    url_prefix = "https://yande.re/post?tags="
    # 爬取初始界面数据
    response = requests.get(url_prefix + tags)
    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text, 'lxml')
    paginator_div = soup.select_one("#paginator > div")
    a_labels = paginator_div.select("a")
    # 获取到最后页数
    last = int(a_labels[-2].attrs["aria-label"][5:])
    print('一共有' + str(last) + '页')
    return last


def get_second_page_urls(page_num, tags):
    # 按页爬取图片的二级页面的链接，并存放到second_page_urls中
    second_page_urls = []
    url_prefix = "https://yande.re/post?tags="
    for page in range(1, page_num + 1):
        time.sleep(0.5)
        print('正在爬取第' + str(page) + '页的二级链接')
        response = requests.get(url_prefix + tags + '&page=' + str(page))
        response.encoding = 'UTF-8'
        soup = BeautifulSoup(response.text, 'lxml')
        ul = soup.select_one("#post-list-posts")
        lis = ul.select("li")
        for li in lis:
            # 二级页面
            link = li.select_one("div").select_one("a").attrs["href"]
            link = 'https://yande.re' + link
            second_page_urls.append(link)
    return second_page_urls


def get_image_urls(second_page_urls):
    image_urls = []
    print('一共有' + str(len(second_page_urls)) + '张图片')
    count = 1
    for url in second_page_urls:
        print('正在爬取第'+str(count)+'张图片的链接')
        count += 1
        # 如果是sample图片要进一步处理，如果不是跳过即可
        response = requests.get(url)
        response.encoding = 'UTF-8'
        soup = BeautifulSoup(response.text, 'lxml')
        a_png = soup.select_one("#png")
        a_jpg = soup.select_one("#highres")
        if a_png is not None:
            image_urls.append(a_png.attrs["href"])
        else:
            image_urls.append(a_jpg.attrs["href"])
    return image_urls


def save_urls(tags, image_urls):
    print('图片保存中...')
    # 保存结果
    with open('.//' + tags + '.txt', "w", encoding="UTF-8", newline="") as file:
        for obj in image_urls:
            file.write(str(obj))
            file.write('\n')


def bye(tags):
    print("爬取完毕")
    print('')
    print('请将软件所在目录下的“' + tags + '.txt' + '”文件内容ctrl+A全部复制')
    print('然后打开Internet Download Manager，点击左上角的“任务”，选择“从剪切板中添加批量下载”')
    print('设置好下载目录后下载即可')
    print('Internet Download Manager下载地址：下载:https://wwks.lanzouy.com/ihasD0o6kx3c 密码:8hmb')
    print('按任意键关闭本窗口...')
    input()


def main():
    tags = welcome()
    page_num = get_the_number_of_page(tags)
    second_page_urls = get_second_page_urls(page_num, tags)
    image_urls = get_image_urls(second_page_urls)
    save_urls(tags, image_urls)
    bye(tags)


if __name__ == '__main__':
    main()
