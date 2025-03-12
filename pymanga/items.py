# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import os

import scrapy


class PymangaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ComicItem(scrapy.Item):
    root_path = scrapy.Field()
    comic_title = scrapy.Field()
    comic_path = scrapy.Field()
    url = scrapy.Field()


class VolumeItem(scrapy.Item):
    comic_path = scrapy.Field()
    comic_title = scrapy.Field()
    volume_title = scrapy.Field()
    volume_path = scrapy.Field()


class PictureItem(scrapy.Item):
    volume_path = scrapy.Field()
    comic_title = scrapy.Field()
    volume_title = scrapy.Field()
    index = scrapy.Field() # start from 1
    referer = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()

    def get_old_path(self, files_store: str) -> str:
        return os.path.join(files_store, self["files"][0]["path"])

    def get_new_path(self, extension=None) -> str:
        if extension is None:
            _, extension = os.path.splitext(self["files"][0]["path"])
        if len(extension) > 0 and extension[0] != '.':
            extension = "." + extension
        if self["volume_title"][0]:
            new_file_name = "_".join([self["comic_title"][0], self["volume_title"][0], str(self["index"][0]).zfill(6) + extension, ])
        else:
            new_file_name = "_".join([self["comic_title"][0], str(self["index"][0]).zfill(6) + extension, ])
        return os.path.join(self["volume_path"][0], new_file_name)


class NewsItem(scrapy.Item):
    root_path = scrapy.Field()
    news_title = scrapy.Field()
    news_path = scrapy.Field()
    url = scrapy.Field()
