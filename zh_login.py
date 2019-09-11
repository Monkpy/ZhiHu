# -*- coding:utf-8 -*-
import requests
from lxml import etree

import zh_get_cookie


class Zh_login(object):

    def __init__(self, cookie):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate',  # 去掉br可以防止乱码
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }
        self.cookie = cookie
        self.url = 'https://www.zhihu.com/'

    def login(self):
        # 真是的大数据是XHR加载的瀑布流数据，也是get请求在json数据里面
        # https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=626118cfaef6d9dd95e5056a5f13429c&desktop=true&page_number=2&limit=6&action=down&after_id=5
        response = requests.get(self.url, headers=self.headers, cookies=self.cookie)
        if response.status_code == 200:
            print(response.text)
        else:
            print('GET HomePage Flase code is %s' % response.status_code)

    def main(self):
        self.login()


if __name__ == '__main__':
    # 调用zh_get_cookie.py来请求cookie，也可以将cookie导入到数据库存放，测试cookie的时效性，然后定期存入|抓取
    zgc = zh_get_cookie.Zhihu()
    cookie = zgc.main()
    print(cookie)
    zh = Zh_login(cookie=cookie)
    zh.main()


