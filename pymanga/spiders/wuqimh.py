# -*- coding: utf-8 -*-
import os
import re
import urllib

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from pymanga import settings
from pymanga.items import ComicItem, VolumeItem, PictureItem
from pymanga.utils.js.decrypter import Decrypter


class WuqimhSpider(scrapy.Spider):
    name = 'wuqimh'
    allowed_domains = ['wuqimh.com']
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
        comic_title = response.xpath("//div[@class='book-title']//h1/text()").extract_first()
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
        for volume_url in response.xpath("//div[@id='chpater-list-1']//ul/li/a/@href").extract():
            real_volume_url = urllib.parse.urlunparse((url_parsed.scheme, url_parsed.hostname, volume_url, "", "", ""))
            yield Request(url=real_volume_url, callback=self.parse_volume_page, meta={'comic_path': comic_path, 'comic_title': comic_title, })

    def parse_volume_page(self, response):
        """parse a volume page"""
        root_path = settings.DOWNLOAD_STORE
        comic_title = response.meta.get("comic_title", response.xpath('//script/text()').re_first('g_comic_name = "(.+)"'))
        comic_path = response.meta.get("comic_path", os.path.join(root_path, comic_title))
        volume_title = response.xpath("//div[@class='w996 title pr']/h2/text()").extract_first()
        volume_path = os.path.join(comic_path, volume_title)
        # scrape volume item
        l = ItemLoader(item=VolumeItem(), response=response)
        l.add_value('comic_path', comic_path)
        l.add_value('comic_title', comic_title)
        l.add_value('volume_title', volume_title)
        l.add_value('volume_path', volume_path)
        yield l.load_item()
        # scrape last volume
        relative_volume_url = response.xpath("//a[@class='prevC']/@href").extract_first()
        # would be `javascript:MHW.core.prevC();` if there's no previous chapter
        if relative_volume_url.find("javascript") < 0:
            prev_volume_url = urllib.parse.urljoin(response.url, relative_volume_url)
            yield Request(url=prev_volume_url, callback=self.parse_volume_page)
        # scrape next volume
        relative_volume_url = response.xpath("//a[@class='nextC']/@href").extract_first()
        # would be `javascript:MHW.core.nextC();` if there's no previous chapter
        if relative_volume_url.find("javascript") < 0:
            next_volume_url = urllib.parse.urljoin(response.url, relative_volume_url)
            yield Request(url=next_volume_url, callback=self.parse_volume_page)
        # scrape picture url for current volume
        # pic_count = int(response.xpath("//script/text()").re("g_max_pic_count = (\d+)")[0]) # use less
        # picture page is same as volume page, except '#'. So process image url directly.
        eval_script = response.xpath("//script").re_first("eval\(function.*") # p,a,c,k,e,d
        pic_url_code_raw = Decrypter.decrypt_by_execjs(eval_script)
        print("=======================================", pic_url_code_raw)
        pic_url_list = re.search("\[(.*)\]", pic_url_code_raw).group(1).split(",")
        for i in range(len(pic_url_list)):
            url = urllib.parse.urljoin("http://images.lancaier.com", re.search("\'(.*)\'", pic_url_list[i]).group(1))
            url = url.replace("\\", "")
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
