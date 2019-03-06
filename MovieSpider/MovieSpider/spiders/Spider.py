#!/usr/bin/env python3
# encoding:utf-8
from scrapy import Spider,Request,Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from ..items import MovieItem
from ..settings import DEFAULT_REQUEST_HEADERS


class movieSpider(Spider):
    name = 'movie'
    allowed_domains = ['hd-trailers.net']  #约束域名
    start_urls = 'http://www.hd-trailers.net' #起始域
    pagecount = [i for i in range(1, 514)]

    def start_requests(self):
        for page in self.pagecount:
            url = '{url}/page/{id}'.format(url=self.start_urls, id=page)
            yield Request(url, callback=self.parse_idx)
            
    def parse_idx(self, response):
        movies = response.xpath(
            '//td[@class="navMain"]/table/tr[2]/td/a[1]/@href'
        ).extract()
        for m in movies:
            movie_url = self.start_urls + m
            movie_name = m[7:-1]
            yield Request(movie_url,meta = {'name':movie_name}, callback = self.parse_movie)

    def parse_movie(self,response):
        name = response.meta['name']
        introduction = response.xpath(
            '//table[@class = "mainTopTable"]/tr/td/p/span/text()'
        ).extract()[0]
        trailers = response.xpath(
            '//tr[@itemprop="trailer"]/td[5]/a/@href'
        ).extract()
        dates = response.xpath(
            '//tr[@itemprop="trailer"]/td[1]/text()'
        ).extract()
        idx = 0
        while idx < len(trailers):
            id = idx
            link = trailers[idx]
            date = dates[idx]

            item = MovieItem()
            for f in item.fields:
                try:
                    item[f] = eval(f)
                except Exception as e:
                    print(e)
            yield item
            idx += 1
