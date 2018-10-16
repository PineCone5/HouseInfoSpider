# -*- coding:utf-8 -*-
from lxml import etree
import requests
import random
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep

class Spider(object):
    def __init__(self):
        self.session = requests.session()
        self.user_agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0']
        self.headers = {}

    # 请求页面
    def request_html(self, url):
        """ 请求页面
        传入需要请求的页面的url
        返回bs4.BeautifulSoup类型的html"""
        self.headers['User-Agent'] = random.choice(self.user_agent_list)
        respon1 = self.session.get(url, headers =self.headers)
        sleep(10)
        html  = BeautifulSoup(respon1.text, 'lxml')
        return html


    def start(self):
        csv_file = open("rent.csv", "wb")
        csv_writer = csv.writer(csv_file, delimiter=',')
        url_str = 'https://wh.58.com/chuzu/pn{}/'
        page = 1
        while True:
            url = url_str.format(page)
            page += 1
            print('正在爬取'+ url)
            html = self.request_html(url)
            print(type(html))
            house_list = html.select(".list > li")

            if not house_list:
                break
            for house in house_list:
                house_title = house.select("h2")[0].string.encode("utf8")  # byte
                house_url = urljoin(url, house.select("a")[0]["href"]) # str
                house_info_list = house_title.split()  # list->byte

                house_location = house_info_list[1]
                house_money = house.select(".money")[0].select("b")[0].string.encode("utf8")
                csv_writer.writerow([house_title, house_location, house_money, house_url])



        csv_file.close()


rant = Spider()
rant.start()







