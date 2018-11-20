# -*- coding: utf-8 -*-
import os
import re
import urllib

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from pymanga import settings
from pymanga.items import ComicItem, VolumeItem, PictureItem


class AiroufanSpider(scrapy.Spider):
    name = 'airoufan'
    allowed_domains = ['airoufan.cc']
    __all_urls = []

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__all_urls.append(url)

    def start_requests(self):
        for url in self.__all_urls:
            yield Request(url=url, callback=self.parse_comic_page)

    def parse(self, response):
        """ This method is here only for fixing warning: must implement all abstract methods"""
        return self.parse_comic_page(response)

    def parse_comic_page(self, response):
        """parse a comic page"""
        root_path = settings.DOWNLOAD_STORE
        # scrape comic item
        comic_title = response.xpath("//h2/a/text()").extract_first()
        comic_title = comic_title.replace(":", "_").replace("!", "_")
        comic_path = os.path.join(root_path, comic_title)
        comic_item_loader = ItemLoader(item=ComicItem(), response=response)
        comic_item_loader.add_value('root_path', root_path)
        comic_item_loader.add_value('comic_title', comic_title)
        comic_item_loader.add_value('comic_path', comic_path)
        comic_item_loader.add_value('url', response.url)
        yield comic_item_loader.load_item()
        # scrape volume item
        volume_title = "gallery"
        volume_path = os.path.join(comic_path, volume_title)
        volume_item_loader = ItemLoader(item=VolumeItem(), response=response)
        volume_item_loader.add_value('comic_path', comic_path)
        volume_item_loader.add_value('comic_title', comic_title)
        volume_item_loader.add_value('volume_title', volume_title)
        volume_item_loader.add_value('volume_path', volume_path)
        yield volume_item_loader.load_item()
        # parse first picture page
        # append meta data manually
        response.meta["comic_title"] = comic_title
        response.meta["volume_title"] = volume_title
        response.meta["volume_path"] = volume_path
        for x in self.parse_picture_page(response):
            yield x

    def parse_picture_page(self, response):
        # parse current picture file
        comic_title = response.meta.get("comic_title")
        volume_title = response.meta.get("volume_title")
        volume_path = response.meta.get("volume_path")
        image_index = 1
        re_result = re.search("/\d+_(\d+).html", response.url)
        if re_result:
            image_index = int(re_result.group(1))
        image_url = response.xpath("//div[@class='content']/div/a/img/@src").extract_first()
        picture_item_loader = ItemLoader(item=PictureItem(), response=response)
        picture_item_loader.add_value("volume_path", volume_path)
        picture_item_loader.add_value("comic_title", comic_title)
        picture_item_loader.add_value("volume_title", volume_title)
        picture_item_loader.add_value("index", image_index)
        picture_item_loader.add_value("referer", response.url)
        picture_item_loader.add_value("file_urls", image_url)
        yield picture_item_loader.load_item()
        # parse next picture page
        next_picture_page_relative_url = response.xpath("//div[@class='tres']/a/@href").extract()[-1]
        if next_picture_page_relative_url != "#":
            # current page is the last page of this volume
            next_picture_page_url = urllib.parse.urljoin(response.url, next_picture_page_relative_url)
            yield Request(url=next_picture_page_url, callback=self.parse_picture_page, meta={
                "comic_title": comic_title,
                "volume_title": volume_title,
                "volume_path": volume_path,
            })


    def parse(self, response):
        pass
