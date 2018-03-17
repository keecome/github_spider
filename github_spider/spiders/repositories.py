# -*- coding: utf-8 -*-
import scrapy
from github_spider.items import RepositoryItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmp = 'https://github.com/phoenixlzx?page={}&tab=repositories'
        return (url_tmp.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.xpath('.//div[@id="user-repositories-list"]/ul/li'):
            item = RepositoryItem()
            item['name'] = repository.xpath('.//a/text()').extract_first().strip()
            item['update_time'] = repository.xpath('.//relative-time/@datetime').extract_first()

            repository_url = response.urljoin(repository.xpath('.//a/@href').extract_first())
            request = scrapy.Request(repository_url, callback=self.parse_repo)
            request.meta['item'] = item

            yield request

    def parse_repo(self, response):
        item = response.meta['item']

        item['commits'] = ''.join(response.xpath('.//a[contains(@href,"commit")]').xpath(
            './/span[@class="num text-emphasized"]/text()').extract_first().strip().split(','))
        item['branches'] = ''.join(response.xpath('.//a[contains(@href,"branch")]').xpath(
            './/span[@class="num text-emphasized"]/text()').extract_first().strip().split(','))
        item['releases'] = ''.join(response.xpath('.//a[contains(@href,"release")]').xpath(
            './/span[@class="num text-emphasized"]/text()').extract_first().strip().split(','))

        yield item
