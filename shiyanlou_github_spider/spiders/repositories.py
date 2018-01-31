# -*- coding: utf-8 -*-
import scrapy
from shiyanlou_github_spider.items import RepositoryItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmp = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmp.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.xpath('.//div[@id="user-repositories-list"]/ul/li'):
            item = RepositoryItem({
                'name': repository.xpath('.//a/text()').extract_first().split(),
                'update_time': repository.xpath('.//relative-time/@datetime').extract_first()
            })
            yield item
