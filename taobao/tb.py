# coding: utf-8
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from pyquery import PyQuery as pq
from selenium import webdriver
import time
import argparse


class GetTiaoBao(object):
    def __init__(self,keyword='iphone'):
        options = Options()
        options.add_argument('-headless')  # 无头参数
        # 使用第三方firfox浏览器驱动
        # self.browser = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)
        self.browser = webdriver.Firefox()
        self.browser.delete_all_cookies()
        self.wait = WebDriverWait(self.browser, 10)
        self.keyword = keyword

    def close(self):
        print("关闭")
        self.browser.close()

    def get_first_page(self):
        print("爬取的商品为:%s" % self.keyword)
        try:
            url = 'https://s.taobao.com/search?q=' + self.keyword
            self.browser.get(url)
        except TimeoutException:
            time.sleep(2)
            self.get_first_page()

    def start_page(self, page):
        """
        抓取索引页
        :param page: 页码
        """
        print("正在抓取第 %s 页" % page)
        try:
            if page > 1:
                input = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'J_Input')))
                submit = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'J_Submit')))
                input.clear()
                input.send_keys(page)
                submit.click()
            else:
                self.get_first_page()
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager  li.item.active > span'),str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            self.get_data()
        except TimeoutException:
            self.start_page(page)


    def get_data(self):
        """提取商品数据"""
        html = self.browser.page_source
        doc = pq(html)
        res = doc('#mainsrp-itemlist .items .item').items()
        product= {}
        for item in res:
            product = {
                'title': item.find('.title').text(),
                #'image': item.find('.pic img').attr('data-src'),
                #'price': item.find('.price').text(),
                #'deal': item.find('.deal-cnt').text(),
                #'shop': item.find('.shop').text(),
                #'location': item.find('.location').text()
             }
            print(product)


def main(k='ipad'):
    run = GetTiaoBao(k)
    for x in range(1,20):
        time.sleep(2)
        run.start_page(x)
    run.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
           description="""
              Selenium Crawl Taobao Product
              Example: \r\n
              python %(prog)s xxx;
              """
      )

    parser.add_argument(
        "product", type=str,nargs="+",
           help="Enter a product",
      )

    args = parser.parse_args()
    p = ' '.join(args.product)
    main(p)
