# -*- coding: utf-8 -*-

import scrapy
from first.items import FirstItem


class FirstSpider(scrapy.Spider):
    # 爬虫名称，唯一
    name = "first"
    # 允许访问的域
    allowed_domains = ["aladd.net"]
    # 初始URL
    start_urls = ['http://aladd.net/archives/32545.html']

    def parse(self, response):
        # 获取所有图片的a标签
        allPics = response.xpath('//div[@class="entry"]/p')[2:]
        for pic in allPics:
            # 分别处理每个图片，取出名称及地址
            item = FirstItem()
            name = pic.xpath('./a/img/@alt').extract()[0]
            url = pic.xpath('./a/img/@src').extract()[0]
            item['name'] = name
            item['url'] = url
            # 返回爬取到的数据
            yield item