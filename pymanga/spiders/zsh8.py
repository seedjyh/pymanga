# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from pymanga import settings
from pymanga.items import ComicItem, VolumeItem, PictureItem


class Zsh8Spider(scrapy.Spider):
    name = 'zsh8'
    allowed_domains = ['zsh8.com']
    __all_urls = []

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__all_urls.append(url)

    def start_requests(self):
        for url in self.__all_urls:
            yield Request(url=url, callback=self.parse_comic_page)

    def parse(self, response):
        """ This method is here only for fixing warning: must implement all abstract methods"""
        pass

    def parse_comic_page(self, response):
        """parse a comic page"""
        root_path = settings.DOWNLOAD_STORE
        comic_title = response.xpath("//span[@class='breadcrumb-leaf']/text()").extract_first()
        comic_title = comic_title.replace(":", "_").replace("!", "_")  # 重复代码
        comic_path = os.path.join(root_path, comic_title)  # 重复代码
        # scrape comic item
        l = ItemLoader(item=ComicItem(), response=response)
        l.add_value('root_path', root_path)
        l.add_value('comic_title', comic_title)
        l.add_value('comic_path', comic_path)
        l.add_value('url', response.url)
        yield l.load_item()
        # scrape volume url
        for item in self.parse_volume_list_page(response, meta={'comic_path': comic_path, 'comic_title': comic_title, }):
            yield item

    def parse_volume_list_page(self, response, meta=None):
        """parse a page with volume list"""
        if meta:
            # called by parse_comic_page
            pass
        else:
            # called by this function itself
            meta = {
                "comic_path": response.meta.get("comic_path"),
                "comic_title": response.meta.get("comic_title"),
            }
        for url in response.xpath("//article/div/div/div/h2/a/@href").extract():
            yield Request(url=url, callback=self.parse_volume_page, meta=meta)
        next_page_url = response.xpath("//a[@class='pagination-next']/@href").extract_first()
        if next_page_url:
            yield Request(url=next_page_url, callback=self.parse_volume_list_page, meta=meta)

    def parse_volume_page(self, response):
        """parse a volume page"""
        comic_title = response.meta.get("comic_title")
        comic_path = response.meta.get("comic_path")
        volume_title = response.xpath("//meta[@property='og:title']/@content").extract_first()
        volume_path = os.path.join(comic_path, volume_title)
        # scrape volume item
        l = ItemLoader(item=VolumeItem(), response=response)
        l.add_value('comic_path', comic_path)
        l.add_value('comic_title', comic_title)
        l.add_value('volume_title', volume_title)
        l.add_value('volume_path', volume_path)
        yield l.load_item()
        # scrape picture url for current volume
        pic_url_list = response.xpath("//dl[@class='gallery-item']/dt/a/@href").extract()
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