#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: seedjyh@gmail.com
# Create date: 2018/10/30
import os
import re
import urllib.parse

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from pymanga import settings
from pymanga.utils.js.decrypter import Decrypter
from pymanga.items import ComicItem, VolumeItem, PictureItem, NewsItem


class DmzjSpider(scrapy.Spider):
    name = 'dmzj'
    allowed_domains = ['dmzj.com']
    all_urls = [
        'https://manhua.dmzj.com/morijianglin/13110.shtml',
    ]

    def start_requests(self):
        for url in self.all_urls:
            url_parsed = urllib.parse.urlparse(url)
            if url_parsed.netloc == 'manhua.dmzj.com':
                if os.path.splitext(url_parsed.path)[1]:
                    yield Request(url=url, callback=self.parse_volume_page)
                else:
                    yield Request(url=url, callback=self.parse_comic_page)
            elif url_parsed.netloc == 'news.dmzj.com':
                yield Request(url=url, callback=self.parse_news_page)

    def parse(self, response):
        """ This method is here only for fixing warning: must implement all abstract methods"""
        return self.parse_comic_page(response)

    def parse_comic_page(self, response):
        """parse a comic page"""
        root_path = settings.DOWNLOAD_STORE
        comic_title = response.xpath('//script/text()').re_first('g_comic_name = "(.+)"')
        comic_title = comic_title.replace(":", "_").replace("!", "_")
        comic_path = os.path.join(root_path, comic_title)
        # scrape comic item
        l = ItemLoader(item=ComicItem(), response=response)
        l.add_value('root_path', root_path)
        l.add_value('comic_title', comic_title)
        l.add_value('comic_path', comic_path)
        l.add_value('url', response.url)
        yield l.load_item()
        # scrape volume url
        url_parsed = urllib.parse.urlparse(response.url)
        for volume_url in response.css('.cartoon_online_border').xpath('ul/li/a/@href').extract():
            real_volume_url = urllib.parse.urlunparse((url_parsed.scheme, url_parsed.hostname, volume_url, "", "", ""))
            yield Request(url=real_volume_url, callback=self.parse_volume_page, meta={'comic_path': comic_path, 'comic_title': comic_title,})

    def parse_volume_page(self, response):
        """parse a volume page"""
        root_path = settings.DOWNLOAD_STORE
        comic_title = response.meta.get("comic_title", response.xpath('//script/text()').re_first('g_comic_name = "(.+)"'))
        comic_path = response.meta.get("comic_path", os.path.join(root_path, comic_title))
        volume_title = response.xpath('//script/text()').re_first('g_chapter_name = "(.*)"')
        volume_path = os.path.join(comic_path, volume_title)
        # scrape volume item
        l = ItemLoader(item=VolumeItem(), response=response)
        l.add_value('comic_path', comic_path)
        l.add_value('comic_title', comic_title)
        l.add_value('volume_title', volume_title)
        l.add_value('volume_path', volume_path)
        yield l.load_item()
        # scrape last volume
        prev_volume_url = urllib.parse.urljoin(response.url, response.xpath("//a[@id='prev_chapter']/@href").extract_first())
        yield Request(url=prev_volume_url, callback=self.parse_volume_page)
        # scrape next volume
        next_volume_url = urllib.parse.urljoin(response.url, response.xpath("//a[@id='next_chapter']/@href").extract_first())
        yield Request(url=next_volume_url, callback=self.parse_volume_page)
        # scrape picture url for current volume
        # pic_count = int(response.xpath("//script/text()").re("g_max_pic_count = (\d+)")[0]) # use less
        # picture page is same as volume page, except '#'. So process image url directly.
        eval_script = response.xpath("//script").re_first("eval\(function.*") # p,a,c,k,e,d
        pic_url_code_raw = Decrypter.decrypt(eval_script)
        pic_url_list = re.search("\[(.*)\]", pic_url_code_raw).group(1).split(",")
        for i in range(len(pic_url_list)):
            url = urllib.parse.urljoin("https://images.dmzj.com", re.search("\"(.*)\"", pic_url_list[i]).group(1))
            url = url.replace("\\", "")
            l = ItemLoader(item=PictureItem(), response=response)
            l.add_value("volume_path", volume_path)
            l.add_value("comic_title", comic_title)
            l.add_value("volume_title", volume_title)
            l.add_value("index", i + 1)
            l.add_value("referer", response.url)
            l.add_value("file_urls", url)
            yield l.load_item()

    def parse_news_page(self, response):
        url_for_all = response.xpath("//a[contains(text(),'在本页阅读全文')]/@href").extract()
        if url_for_all:
            yield Request(url=url_for_all[0], callback=self.parse_news_page_all)
        else:
            for v in self.parse_news_page_all(response):
                yield v

    def parse_news_page_all(self, response):
        """parse a news page"""
        root_path = settings.DOWNLOAD_STORE
        news_title = response.xpath('//h1/text()').extract_first()
        news_title = news_title.replace(":", "_").replace("!", "_")
        news_path = os.path.join(root_path, news_title)
        # scrape news item
        l = ItemLoader(item=NewsItem(), response=response)
        l.add_value('root_path', root_path)
        l.add_value('news_title', news_title)
        l.add_value('news_path', news_path)
        l.add_value('url', response.url)
        yield l.load_item()
        # more variable
        comic_path = news_path
        comic_title = news_title
        volume_title = ""  # empty means no volume title
        volume_path = comic_path
        # scrape picture url
        pic_url_list = response.xpath("//div[@class='news_content_con']/p[@style='text-align:center']/img/@src").extract()
        for i in range(len(pic_url_list)):
            url = pic_url_list[i]
            l = ItemLoader(item=PictureItem(), response=response)
            l.add_value("volume_path", volume_path)
            l.add_value("comic_title", comic_title)
            l.add_value("volume_title", volume_title)
            l.add_value("index", i + 1)
            l.add_value("referer", response.url)
            l.add_value("file_urls", url)
            yield l.load_item()


if __name__ == "__main__":
    pass
