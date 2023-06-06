from PoolSpider import crawl_pool
from PostSpider import crawl_post

def main():
    print("欢迎使用芙咪莉儿的Yande图片批量爬取器")
    print("B站ID：芙咪莉儿")
    print("")
    print("[1] Posts（批量爬取插画，https://yande.re/post）")
    print("[2] Pools（批量爬取画集，https://yande.re/pool）")
    print("请选择需要爬取的版块：", end='')

    select = input()
    if select == "1":
        crawl_post()
    elif select == "2":
        crawl_pool()
    else:
        print("无法识别选项")
    print("键入任意键后退出...")
    input()


if __name__ == "__main__":
    main()
