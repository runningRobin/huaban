import scrapy
from scrapy import selector
from urllib import request
import random
import string
import os


class HuaBanSpider(scrapy.Spider):
    name = 'huaban'
    allowed_domain   = ['www.meisupic.com']
    start_url = 'http://www.meisupic.com/topic.php'
    download_path = 'D:/huaban_img/'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    headers = {'User-Agent': user_agent}

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, headers=self.headers, method='GET', callback=self.parse)

    def parse(self, response):
        lists = response.selector.xpath('//ul[@class="slides"]/li/dl/a')
        for cate in lists:
            cate_info_url = 'http://www.meisupic.com/' + cate.xpath('@href').extract()[0]
            yield scrapy.Request(url=cate_info_url, headers=self.headers, method='GET', callback=self.topic_parse)

    def topic_parse(self, response):
        lists = response.selector.xpath('//ul[@class="imgList"]/li/a/img')
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        for imgage in lists:
            img_url = imgage.xpath('@data-original').extract()[0]
            name = ''.join(random.sample(string.ascii_letters + string.digits, 12))
            path = self.download_path + name + '.jpg'
            request.urlretrieve(img_url, path)

